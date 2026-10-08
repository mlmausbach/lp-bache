/* Consentimento de cookies do bache.com.br (LGPD, art. 7º, I, e o guia de cookies da ANPD).
 *
 * Quatro regras, todas cobertas por tests/js.test.mjs e tests/test_cookies.py:
 *   1. Estatística e marketing nascem desligados.
 *   2. O Google Tag Manager (hoje só o GA4 mora nele) só é carregado depois que o
 *      visitante aceita pelo menos uma categoria. Antes disso nenhum pedido sai para o Google.
 *   3. Recusar custa o mesmo que aceitar: os dois são botões do mesmo tamanho, na mesma linha.
 *   4. A escolha vale 12 meses, fica só neste navegador e se muda pelo rodapé de qualquer página.
 *
 * A categoria Marketing existe no código e some da tela: o container só tem o GA4 (conferido em 08/10/2026), e pedir consentimento
 * para o que não existe seria consentimento genérico (LGPD, art. 8º, §4º). Quando entrar uma tag de anúncio: caixa ck-marketing no
 * bloco comum, linha na política e na tabela de cookies, o teste em tests/test_cookies.py e VERSAO + 1 aqui: a política promete
 * que a escolha volta a ser pedida quando entrar um cookie novo, e só subir a VERSAO cumpre isso.
 *
 * No navegador vira window.bacheConsent; no Node, module.exports (tests/js.test.mjs).
 */
(function () {
  'use strict';

  var CHAVE = 'bache-cookies';
  var VERSAO = 1;
  var VALIDADE = 365 * 24 * 3600 * 1000;
  var GTM_ID = 'GTM-P7VS3KVG';

  /* Os cookies que cada categoria pode deixar neste domínio. Sem o consentimento, nenhum nasce. */
  var COOKIES = {
    estatisticas: ['_ga', '_ga_*', '_gid', '_gat', '_gat_*'],
    marketing: ['_gcl_au', '_gcl_aw', '_gcl_dc', '_gcl_gb', '_gcl_ha', '_gac_*']
  };

  function lerEscolha(storage, agora) {
    var e;
    try {
      var cru = storage.getItem(CHAVE);
      if (!cru) return null;
      e = JSON.parse(cru);
    } catch (erro) { return null; }
    if (!e || e.v !== VERSAO || typeof e.t !== 'number') return null;
    if (agora - e.t > VALIDADE) return null;
    return { estatisticas: e.estatisticas === true, marketing: e.marketing === true, t: e.t };
  }

  function gravarEscolha(storage, escolha, agora) {
    var e = { v: VERSAO, t: agora, estatisticas: !!escolha && escolha.estatisticas === true, marketing: !!escolha && escolha.marketing === true };
    try { storage.setItem(CHAVE, JSON.stringify(e)); } catch (erro) { /* navegador que bloqueia o storage: pergunta de novo na próxima visita */ }
    return e;
  }

  /* O Consent Mode do Google: tudo negado até o visitante dizer o contrário. */
  function estadoGoogle(escolha) {
    var est = !!escolha && escolha.estatisticas === true;
    var mkt = !!escolha && escolha.marketing === true;
    return {
      analytics_storage: est ? 'granted' : 'denied',
      ad_storage: mkt ? 'granted' : 'denied',
      ad_user_data: mkt ? 'granted' : 'denied',
      ad_personalization: mkt ? 'granted' : 'denied',
      functionality_storage: 'granted',
      security_storage: 'granted'
    };
  }

  function deveCarregarGTM(escolha) {
    return !!escolha && (escolha.estatisticas === true || escolha.marketing === true);
  }

  /* Quem tirou uma categoria leva embora os cookies dela, e só os dela. */
  function cookiesParaApagar(antes, depois) {
    if (!antes) return [];
    var lista = [];
    ['estatisticas', 'marketing'].forEach(function (c) {
      if (antes[c] === true && !(depois && depois[c] === true)) lista = lista.concat(COOKIES[c]);
    });
    return lista;
  }

  var api = {
    CHAVE: CHAVE, VERSAO: VERSAO, VALIDADE: VALIDADE, GTM_ID: GTM_ID,
    lerEscolha: lerEscolha, gravarEscolha: gravarEscolha, estadoGoogle: estadoGoogle,
    deveCarregarGTM: deveCarregarGTM, cookiesParaApagar: cookiesParaApagar
  };

  if (typeof window === 'undefined') {
    if (typeof module === 'object' && module.exports) module.exports = api;
    return;
  }

  /* ---- navegador ---- */
  var w = window;
  var d = document;
  var banner, prefs, caixaEst, caixaMkt;
  var gtmCarregado = false;
  w.dataLayer = w.dataLayer || [];
  function gtag() { w.dataLayer.push(arguments); }

  function armazenamento() {
    try { return w.localStorage; } catch (erro) { return { getItem: function () { return null; }, setItem: function () {} }; }
  }

  function carregarGTM() {
    if (gtmCarregado) return;
    gtmCarregado = true;
    w.dataLayer.push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
    var s = d.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtm.js?id=' + GTM_ID;
    d.head.appendChild(s);
  }

  function apagarCookie(padrao) {
    var nomes = [];
    d.cookie.split(';').forEach(function (par) {
      var n = par.split('=')[0].replace(/^\s+/, '');
      if (!n) return;
      var casa = padrao.charAt(padrao.length - 1) === '*' ? n.indexOf(padrao.slice(0, -1)) === 0 : n === padrao;
      if (casa) nomes.push(n);
    });
    var host = w.location.hostname;
    var partes = host.split('.');
    var dominios = [null];
    for (var i = 0; i < partes.length - 1; i++) dominios.push('.' + partes.slice(i).join('.'));
    nomes.forEach(function (n) {
      dominios.forEach(function (dom) {
        d.cookie = n + '=; Max-Age=0; path=/' + (dom ? '; domain=' + dom : '') + '; SameSite=Lax';
      });
    });
  }

  function sincronizarCaixas(escolha) {
    caixaEst.checked = !!escolha && escolha.estatisticas === true;
    if (caixaMkt) caixaMkt.checked = !!escolha && escolha.marketing === true;
  }

  function abrirPreferencias() {
    sincronizarCaixas(lerEscolha(armazenamento(), new Date().getTime()));
    if (typeof prefs.showModal === 'function') { if (!prefs.open) prefs.showModal(); }
    else prefs.setAttribute('open', '');
  }

  function fecharPreferencias() {
    if (typeof prefs.close === 'function') prefs.close();
    else prefs.removeAttribute('open');
  }

  function aplicar(nova, anterior) {
    var gravada = gravarEscolha(armazenamento(), nova, new Date().getTime());
    gtag('consent', 'update', estadoGoogle(gravada));
    if (deveCarregarGTM(gravada)) carregarGTM();
    cookiesParaApagar(anterior, gravada).forEach(apagarCookie);
    w.dataLayer.push({ event: 'consent_atualizado', consent_estatisticas: gravada.estatisticas, consent_marketing: gravada.marketing });
    banner.hidden = true;
    fecharPreferencias();
  }

  function aoClicar(acao) {
    var anterior = lerEscolha(armazenamento(), new Date().getTime());
    if (acao === 'aceitar') aplicar({ estatisticas: true, marketing: !!caixaMkt }, anterior);
    else if (acao === 'recusar') aplicar({ estatisticas: false, marketing: false }, anterior);
    else if (acao === 'salvar') aplicar({ estatisticas: caixaEst.checked, marketing: !!caixaMkt && caixaMkt.checked }, anterior);
    else if (acao === 'personalizar') abrirPreferencias();
    else if (acao === 'fechar') fecharPreferencias();
  }

  function iniciar() {
    banner = d.getElementById('cookies');
    prefs = d.getElementById('cookies-prefs');
    caixaEst = d.getElementById('ck-estatisticas');
    caixaMkt = d.getElementById('ck-marketing');
    if (!banner || !prefs || !caixaEst) return;

    d.querySelectorAll('[data-cookies]').forEach(function (b) {
      b.addEventListener('click', function () { aoClicar(b.getAttribute('data-cookies')); });
    });
    d.querySelectorAll('[data-cookies-abrir]').forEach(function (b) {
      b.addEventListener('click', abrirPreferencias);
    });

    var escolha = lerEscolha(armazenamento(), new Date().getTime());
    if (escolha) {
      gtag('consent', 'update', estadoGoogle(escolha));
      if (deveCarregarGTM(escolha)) carregarGTM();
    } else {
      banner.hidden = false;
    }
  }

  /* Tudo negado antes de qualquer outra coisa, e antes de o GTM existir na página. */
  gtag('consent', 'default', estadoGoogle(null));

  w.bacheConsent = api;
  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', iniciar);
  else iniciar();
})();
