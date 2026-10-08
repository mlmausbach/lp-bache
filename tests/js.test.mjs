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

// ---- consentimento de cookies (assets/js/consent.js, doc 12 §8) ----
const consent = require('../assets/js/consent.js');
const MES = 30 * 24 * 3600 * 1000;
const memoria = () => { const m = {}; return { getItem: k => (k in m ? m[k] : null), setItem: (k, v) => { m[k] = String(v); }, removeItem: k => { delete m[k]; } }; };
const quebrado = { getItem() { throw new Error('bloqueado'); }, setItem() { throw new Error('bloqueado'); } };

test('consentimento: sem registro, pergunta', () => {
  assert.equal(consent.lerEscolha(memoria(), 1000), null);
});

test('consentimento: registro quebrado, de outra versão ou vencido volta a perguntar', () => {
  const s = memoria();
  s.setItem(consent.CHAVE, '{nao é json');
  assert.equal(consent.lerEscolha(s, 1000), null);
  s.setItem(consent.CHAVE, JSON.stringify({ v: 99, t: 1000, estatisticas: true, marketing: true }));
  assert.equal(consent.lerEscolha(s, 2000), null);
  s.setItem(consent.CHAVE, JSON.stringify({ v: consent.VERSAO, t: 1000, estatisticas: true, marketing: true }));
  assert.equal(consent.lerEscolha(s, 1000 + 13 * MES), null);
});

test('consentimento: grava e lê a escolha, só com booleanos', () => {
  const s = memoria();
  consent.gravarEscolha(s, { estatisticas: true, marketing: 'sim' }, 5000);
  const e = consent.lerEscolha(s, 6000);
  assert.deepEqual({ estatisticas: e.estatisticas, marketing: e.marketing }, { estatisticas: true, marketing: false });
});

test('consentimento: navegador que bloqueia o storage não derruba nada', () => {
  assert.equal(consent.lerEscolha(quebrado, 1000), null);
  assert.doesNotThrow(() => consent.gravarEscolha(quebrado, { estatisticas: true, marketing: true }, 1000));
});

test('consentimento: o estado do Google nasce todo negado, e cada categoria liga o seu grupo', () => {
  const nada = consent.estadoGoogle({ estatisticas: false, marketing: false });
  assert.equal(nada.analytics_storage, 'denied');
  for (const k of ['ad_storage', 'ad_user_data', 'ad_personalization']) assert.equal(nada[k], 'denied');
  const est = consent.estadoGoogle({ estatisticas: true, marketing: false });
  assert.equal(est.analytics_storage, 'granted');
  assert.equal(est.ad_storage, 'denied');
  const mkt = consent.estadoGoogle({ estatisticas: false, marketing: true });
  assert.equal(mkt.analytics_storage, 'denied');
  for (const k of ['ad_storage', 'ad_user_data', 'ad_personalization']) assert.equal(mkt[k], 'granted');
  assert.deepEqual(consent.estadoGoogle(null), nada);
});

test('consentimento: o GTM só carrega com pelo menos uma categoria aceita', () => {
  assert.equal(consent.deveCarregarGTM(null), false);
  assert.equal(consent.deveCarregarGTM({ estatisticas: false, marketing: false }), false);
  assert.equal(consent.deveCarregarGTM({ estatisticas: true, marketing: false }), true);
  assert.equal(consent.deveCarregarGTM({ estatisticas: false, marketing: true }), true);
});

test('consentimento: tirar uma categoria apaga os cookies dela, e só dela', () => {
  const antes = { estatisticas: true, marketing: true };
  assert.deepEqual(consent.cookiesParaApagar(antes, { estatisticas: true, marketing: true }), []);
  const semEst = consent.cookiesParaApagar(antes, { estatisticas: false, marketing: true });
  assert.ok(semEst.includes('_ga') && semEst.includes('_ga_*') && !semEst.some(n => n.startsWith('_gcl')));
  const semMkt = consent.cookiesParaApagar(antes, { estatisticas: true, marketing: false });
  assert.ok(semMkt.includes('_gcl_au') && !semMkt.includes('_ga'));
  assert.deepEqual(consent.cookiesParaApagar(null, { estatisticas: false, marketing: false }), []);
});
