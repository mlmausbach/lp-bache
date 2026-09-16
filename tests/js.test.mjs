// As duas regras de negócio em JS: o fit do pedido (assets/js/fit.js) e a
// tarefa que o Worker cria no ClickUp (worker/lead.js).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { lead } from '../worker/lead.js';

const require = createRequire(import.meta.url);
const { calcularFit } = require('../assets/js/fit.js');

const resp = (fat, origem, nota) => ({ fat: { v: fat }, origem: { v: origem }, nota: { v: nota } });

test('fit: acima de R$ 80 mil com os dois sinais é quente', () => {
  assert.equal(calcularFit(resp('80-150', 'indicacao', '45+')).fit, 'quente');
});

test('fit: entre R$ 50 e 80 mil é morno', () => {
  assert.equal(calcularFit(resp('50-80', 'google', 'abaixo')).fit, 'morno');
});

test('fit: abaixo de R$ 50 mil é frio, mesmo com os dois sinais', () => {
  assert.equal(calcularFit(resp('ate-50', 'indicacao', '45+')).fit, 'frio');
});

test('lead do médico descreve o faturamento do consultório, sem orçamento', async () => {
  let tarefa;
  globalThis.fetch = async (url, init) => {
    if (String(url).endsWith('/task')) tarefa = JSON.parse(init.body);
    return new Response(JSON.stringify({ id: 't1' }), { status: 200 });
  };
  const pedido = new Request('https://bache.com.br/api/lead', {
    method: 'POST',
    body: JSON.stringify({
      path: 'med', nome: 'Ana Teste', whatsapp: '(41) 99999-0000', email: 'ana@exemplo.com.br',
      faturamento: 'R$ 80 a 150 mil', score: 9,
    }),
  });
  const resposta = await lead(pedido, { CLICKUP_TOKEN: 'teste' });
  assert.equal(resposta.status, 200);
  assert.match(tarefa.description, /Faturamento do consultório por mês: R\$ 80 a 150 mil/);
  assert.doesNotMatch(tarefa.description, /rçamento/);
});
