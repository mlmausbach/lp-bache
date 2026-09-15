/* Recebe o pedido de Raio-X do formulário e cria a tarefa no ClickUp.
 *
 * Até 15/09/2026 o navegador falava direto com a API do ClickUp, e o token
 * pessoal ficava escrito no HTML público (e no histórico do repo, que é
 * público). Agora o token é secret do Pages (CLICKUP_TOKEN) e só existe
 * dentro desta função, no servidor.
 *
 * O formulário fala com /api/lead, não com o ClickUp: trocar o destino do
 * lead depois é mexer neste arquivo, não na página.
 */

const API = 'https://api.clickup.com/api/v2';
const LISTA = '901111231101'; // Sessão Estratégica
const CAMPO_WHATSAPP = '72a107e8-d809-4417-89bf-1036ce89c88a';
const CAMPO_EMAIL = 'fd5e499d-be16-4941-b14d-c4bf5dcbe776';

function json(dados, status) {
  return new Response(JSON.stringify(dados), {
    status: status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
    },
  });
}

/* Todo campo chega do navegador, então é texto não confiável: uma linha só,
   sem espaço sobrando, com teto de tamanho. */
function texto(v, max) {
  return String(v == null ? '' : v).replace(/\s+/g, ' ').trim().slice(0, max);
}

/* Validação proposital: não tenta ser RFC 5322. Só recusa o que claramente
   não é endereço. */
function emailPlausivel(v) {
  return v.length >= 6 && v.length <= 254 && /^[^\s@]+@[^\s@.]+\.[^\s@]{2,}$/.test(v);
}

/* 10 ou 11 dígitos é número nacional (DDD + telefone), então ganha o 55.
   12 ou 13 começando com 55 já veio com o código do país. Olhar só o
   prefixo 55 confundiria o DDD 55 do Rio Grande do Sul com o código. */
function whatsappInternacional(digitos) {
  if (digitos.length >= 12 && digitos.startsWith('55')) return '+' + digitos;
  return '+55' + digitos;
}

export async function onRequest({ request, env }) {
  /* Um handler só. Exportar onRequest e onRequestPost juntos deixa o
     roteamento do Pages ambíguo. */
  if (request.method !== 'POST') return json({ ok: false, erro: 'metodo' }, 405);

  let c;
  try {
    c = await request.json();
  } catch (e) {
    return json({ ok: false, erro: 'formato' }, 400);
  }
  if (!c || typeof c !== 'object') return json({ ok: false, erro: 'formato' }, 400);

  /* Campo isca: humano nunca preenche, robô de formulário quase sempre.
     Responde 200 pro robô não descobrir que foi barrado. */
  if (c.empresa) return json({ ok: true }, 200);

  const clinica = c.path === 'cli';
  const lead = {
    nome: texto(c.nome, 120),
    whatsapp: texto(c.whatsapp, 30),
    email: texto(c.email, 254).toLowerCase(),
    cidade: texto(c.cidade, 80),
    especialidade: texto(c.especialidade, 160),
    atendimento: texto(c.atendimento, 80),
    onde: texto(c.onde, 80),
    nMedicos: texto(c.nMedicos, 80),
    papel: texto(c.papel, 80),
    faturamento: texto(c.faturamento, 80),
    marketing: texto(c.marketing, 80),
    conteudo: texto(c.conteudo, 80),
    gargalo: texto(c.gargalo, 120),
  };
  const digitos = lead.whatsapp.replace(/\D/g, '');

  if (!lead.nome || digitos.length < 10 || digitos.length > 13 || !emailPlausivel(lead.email)) {
    return json({ ok: false, erro: 'campos' }, 400);
  }

  if (!env.CLICKUP_TOKEN) {
    /* Sem o token a função não inventa sucesso: quem pediu o Raio-X precisa
       saber que o pedido não foi guardado, e a tela oferece o WhatsApp. */
    return json({ ok: false, erro: 'indisponivel' }, 503);
  }

  /* O score só decide a prioridade da tarefa, então vir do navegador não
     abre brecha. O fit é recalculado aqui com a mesma régua da página. */
  const score = Number.isFinite(+c.score) ? Math.max(0, Math.min(99, Math.round(+c.score))) : 0;
  const fit = score >= 8 ? 'quente' : (score >= 5 ? 'morno' : 'frio');
  const prioridade = fit === 'quente' ? 1 : (fit === 'morno' ? 2 : 3);
  const tipo = clinica ? 'Clínica' : 'Médico';
  const ou = v => v || '—';

  const linhas = [
    `Lead via Landing Page — ${tipo}`, '',
    `Fit: ${fit.toUpperCase()} (score ${score})`, '',
    `Nome: ${lead.nome}`, `WhatsApp: ${lead.whatsapp}`, `E-mail: ${lead.email}`,
    `Cidade: ${ou(lead.cidade)}`, `Especialidade(s): ${ou(lead.especialidade)}`, '',
  ];
  if (clinica) {
    linhas.push(`Nº de médicos: ${ou(lead.nMedicos)}`, `Papel: ${ou(lead.papel)}`,
      `Faturamento da clínica: ${ou(lead.faturamento)}`, `Marketing: ${ou(lead.marketing)}`);
  } else {
    linhas.push(`Atendimento: ${ou(lead.atendimento)}`, `Onde atua: ${ou(lead.onde)}`,
      `Faturamento particular: ${ou(lead.faturamento)}`, `Conteúdo/câmera: ${ou(lead.conteudo)}`);
  }
  linhas.push(`Maior gargalo: ${ou(lead.gargalo)}`);

  const cabecalho = { Authorization: env.CLICKUP_TOKEN, 'Content-Type': 'application/json' };

  let resposta;
  try {
    resposta = await fetch(`${API}/list/${LISTA}/task`, {
      method: 'POST',
      headers: cabecalho,
      body: JSON.stringify({
        name: `Sessão Estratégica — ${lead.nome} (${tipo})`,
        description: linhas.join('\n'),
        priority: prioridade,
      }),
    });
  } catch (e) {
    return json({ ok: false, erro: 'rede' }, 502);
  }

  /* O erro do ClickUp não volta pro navegador: pode conter detalhe da conta.
     Só o suficiente pra tela decidir o que dizer. */
  if (!resposta.ok) return json({ ok: false, erro: 'upstream' }, 502);

  const tarefa = await resposta.json().catch(() => null);
  if (tarefa && tarefa.id) {
    /* Os campos personalizados são conveniência: a descrição já leva
       WhatsApp e e-mail, então falha aqui não derruba o pedido. */
    await Promise.allSettled([
      fetch(`${API}/task/${tarefa.id}/field/${CAMPO_WHATSAPP}`, {
        method: 'POST', headers: cabecalho,
        body: JSON.stringify({ value: whatsappInternacional(digitos) }),
      }),
      fetch(`${API}/task/${tarefa.id}/field/${CAMPO_EMAIL}`, {
        method: 'POST', headers: cabecalho,
        body: JSON.stringify({ value: lead.email }),
      }),
    ]);
  }

  return json({ ok: true }, 200);
}
