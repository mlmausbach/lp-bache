/* bache.com.br · a página: entrada das seções, medição e o formulário do Raio-X.
 *
 * O pedido vai para /api/lead (worker/lead.js), que cria a tarefa na Pipeline
 * Comercial do ClickUp. Nenhuma chave mora nesta página.
 * Os nomes dos eventos (abrir_modal_diagnostico, generate_lead, whatsapp_click)
 * são os mesmos do site anterior, para o GA4 não perder a série.
 */
(function () {
  'use strict';

  var d = document;
  function track(evento, params) { if (window.bacheTrack) window.bacheTrack(evento, params || {}); }
  function el(id) { return d.getElementById(id); }

  /* ── Entrada das seções: só com html.anim, que o <head> liga ── */
  var sobe = d.querySelectorAll('.l-sobe');
  if (d.documentElement.classList.contains('anim') && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -6% 0px' });
    sobe.forEach(function (n) { io.observe(n); });
  } else {
    sobe.forEach(function (n) { n.classList.add('is-in'); });
  }

  /* ── WhatsApp ── */
  d.querySelectorAll('a[href*="wa.me"]:not([data-raio-x])').forEach(function (a) {
    a.addEventListener('click', function () { track('whatsapp_click'); });
  });

  /* ── O formulário ── */
  var dlg = el('raio-x-form');
  /* Sem <dialog>, o botão segue o próprio link: o fecho da página tem o WhatsApp. */
  if (!dlg || typeof dlg.showModal !== 'function') return;

  var form = dlg.querySelector('form');
  var PASSOS = ['bifurca', 'perfil', 'numeros', 'contato'];
  var i = 0;
  var caminho = null;
  var resp = {};
  var rot = el('rx-rot'), barra = el('rx-barra'), etapa = el('rx-etapa');
  var voltar = el('rx-voltar'), erro = el('rx-erro'), enviar = el('rx-enviar');

  function abrir(e) {
    if (e) e.preventDefault();
    if (!dlg.open) dlg.showModal();
    track('abrir_modal_diagnostico');
    mostrar();
  }
  d.querySelectorAll('[data-raio-x]').forEach(function (b) { b.addEventListener('click', abrir); });
  dlg.querySelector('.o-modal__fechar').addEventListener('click', function () { dlg.close(); });
  dlg.querySelectorAll('[data-fechar]').forEach(function (b) { b.addEventListener('click', function () { dlg.close(); }); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });

  /* Cada grupo de opções guarda uma resposta só. */
  form.querySelectorAll('.o-opcoes').forEach(function (g) {
    g.addEventListener('click', function (e) {
      var b = e.target.closest('.o-op');
      if (!b) return;
      g.querySelectorAll('.o-op').forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
      b.setAttribute('aria-pressed', 'true');
      g.classList.remove('is-erro');
      resp[g.dataset.grupo] = { v: b.dataset.v, rotulo: b.dataset.rotulo };
      if (g.dataset.grupo === 'path') {
        caminho = b.dataset.v;
        form.querySelectorAll('[data-so]').forEach(function (n) { n.hidden = n.dataset.so !== caminho; });
        /* A troca de caminho pode esconder a opção marcada num grupo já respondido: ela sai do resp também. */
        form.querySelectorAll('.o-opcoes').forEach(function (og) {
          var marcado = og.querySelector('.o-op[aria-pressed="true"]');
          if (marcado && marcado.hidden) {
            marcado.setAttribute('aria-pressed', 'false');
            delete resp[og.dataset.grupo];
          }
        });
      }
    });
  });

  /* Na /medicos o caminho já vem marcado (<body data-caminho="med">). A pessoa ainda pode trocar. */
  var marcado = d.body.getAttribute('data-caminho');
  if (marcado) {
    var op = form.querySelector('.o-opcoes[data-grupo="path"] .o-op[data-v="' + marcado + '"]');
    if (op) op.click();
  }

  function mostrar() {
    var k = PASSOS[i];
    form.querySelectorAll('.o-passo').forEach(function (p) { p.classList.toggle('is-on', p.dataset.passo === k); });
    etapa.textContent = 'Etapa ' + (i + 1) + ' de ' + PASSOS.length;
    barra.style.width = ((i + 1) / PASSOS.length * 100) + '%';
    voltar.hidden = i === 0;
    rot.textContent = i === PASSOS.length - 1 ? 'Quero meu Raio-X' : 'Continuar';
    erro.hidden = true;
    var foco = form.querySelector('.o-passo.is-on .o-op:not([hidden]), .o-passo.is-on input');
    if (foco) setTimeout(function () { foco.focus(); }, 30);
  }
  voltar.addEventListener('click', function () { if (i > 0) { i--; mostrar(); } });

  /* O que cada etapa exige, por caminho. */
  var EXIGE = {
    bifurca: { campos: ['rx-cidade'], grupos: ['path'] },
    perfil: {
      cli: { campos: ['rx-espec-cli'], grupos: ['nmed', 'papel'] },
      med: { campos: ['rx-espec'], grupos: ['atend', 'onde'] }
    },
    numeros: {
      cli: { grupos: ['fat', 'origem', 'nota', 'gar'] },
      med: { grupos: ['fat', 'origem', 'nota', 'gar'] }
    },
    contato: { campos: ['rx-nome', 'rx-whats', 'rx-email'] }
  };
  function regra(k) { var r = EXIGE[k]; return (r.cli || r.med) ? (r[caminho] || {}) : r; }

  function campoOk(input) {
    var v = input.value.trim();
    var ok = v !== '';
    if (ok && input.type === 'email') ok = /^[^\s@]+@[^\s@.]+\.[^\s@]{2,}$/.test(v);
    if (ok && input.type === 'tel') ok = v.replace(/\D/g, '').length >= 10;
    input.closest('.o-campo').classList.toggle('is-erro', !ok);
    return ok;
  }
  function conferir() {
    var r = regra(PASSOS[i]);
    var ok = true;
    (r.campos || []).forEach(function (id) { if (!campoOk(el(id))) ok = false; });
    (r.grupos || []).forEach(function (g) {
      var tem = !!resp[g];
      form.querySelector('.o-opcoes[data-grupo="' + g + '"]').classList.toggle('is-erro', !tem);
      if (!tem) ok = false;
    });
    if (!ok) { erro.textContent = 'Falta responder o que está marcado.'; erro.hidden = false; }
    else erro.hidden = true;
    return ok;
  }

  /* O fit mora em assets/js/fit.js, que carrega antes deste arquivo. */
  function rotulo(g) { return (resp[g] || {}).rotulo || ''; }
  function valor(id) { var n = el(id); return n ? n.value.trim() : ''; }

  function mostrarErro(codigo) {
    erro.textContent = 'Não deu para registrar o pedido agora (' + codigo + '). ';
    var a = d.createElement('a');
    a.href = 'https://wa.me/5541998416681?text=' + encodeURIComponent('Olá! Tentei pedir o Raio-X pelo site e não foi.');
    a.target = '_blank';
    a.rel = 'noopener';
    a.textContent = 'Fale pelo WhatsApp';
    erro.appendChild(a);
    erro.appendChild(d.createTextNode(' e a gente marca por lá.'));
    erro.hidden = false;
  }

  function enviarPedido() {
    /* Sem o fit.js (falha de rede, bloqueio), o pedido ainda sai, com o fit mais frio. */
    var f = window.bacheFit ? window.bacheFit(resp) : { fit: 'frio', score: 2 };
    var corpo = {
      path: caminho,
      cidade: valor('rx-cidade'),
      especialidade: caminho === 'cli' ? valor('rx-espec-cli') : valor('rx-espec'),
      nMedicos: rotulo('nmed'), papel: rotulo('papel'),
      atendimento: rotulo('atend'), onde: rotulo('onde'),
      faturamento: rotulo('fat'),
      origem: rotulo('origem'), nota: rotulo('nota'), gargalo: rotulo('gar'),
      nome: valor('rx-nome'), whatsapp: valor('rx-whats'), email: valor('rx-email'),
      score: f.score,
      empresa: valor('rx-empresa')
    };
    enviar.disabled = true;
    rot.textContent = 'Enviando';
    fetch('/api/lead', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(corpo)
    })
      .then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (j) {
          if (!r.ok || !j.ok) throw new Error(j.erro || ('HTTP ' + r.status));
        });
      })
      .then(function () {
        form.hidden = true;
        el('rx-ok').hidden = false;
        track('generate_lead', { method: 'form_diagnostico', path: caminho, fit: f.fit });
      })
      .catch(function (e) { mostrarErro(e.message); })
      .then(function () { enviar.disabled = false; rot.textContent = 'Quero meu Raio-X'; });
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!conferir()) return;
    if (i < PASSOS.length - 1) { i++; mostrar(); } else enviarPedido();
  });

  /* Máscara do WhatsApp: (XX) XXXXX-XXXX */
  var whats = el('rx-whats');
  whats.addEventListener('input', function () {
    var n = whats.value.replace(/\D/g, '').slice(0, 11);
    var m = n.length === 0 ? '' :
      n.length <= 2 ? '(' + n :
      n.length <= 7 ? '(' + n.slice(0, 2) + ') ' + n.slice(2) :
      '(' + n.slice(0, 2) + ') ' + n.slice(2, 7) + '-' + n.slice(7);
    whats.value = m;
  });
  form.querySelectorAll('input').forEach(function (n) {
    n.addEventListener('input', function () { var c = n.closest('.o-campo'); if (c) c.classList.remove('is-erro'); });
  });
})();
