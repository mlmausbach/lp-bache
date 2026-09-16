/* O fit do pedido de Raio-X: decide a temperatura e a prioridade da tarefa.
 *
 * Os pisos são os do 16-OFERTAS: R$ 50 mil para o Raio-X, R$ 80 mil para a
 * Instalação. Desde 16/09/2026 (doc 11, decisão 12) a clínica e o médico são
 * medidos igual, pelo faturamento. Os dois sinais são os do templates/01.
 * No navegador vira window.bacheFit; no Node, module.exports (tests/js.test.mjs).
 */
(function (raiz) {
  'use strict';
  var NIVEL = { 'ate-50': 0, '50-80': 1, '80-150': 2, '150+': 2 };

  function calcularFit(resp) {
    var nivel = NIVEL[(resp.fat || {}).v];
    var sinais = ((resp.origem || {}).v === 'indicacao' ? 1 : 0) +
      (['45+', 'sem'].indexOf((resp.nota || {}).v) >= 0 ? 1 : 0);
    if (nivel === 2 && sinais === 2) return { fit: 'quente', score: 9 };
    if (nivel >= 1) return { fit: 'morno', score: 6 };
    return { fit: 'frio', score: 2 };
  }

  if (typeof module === 'object' && module.exports) module.exports = { calcularFit: calcularFit };
  else raiz.bacheFit = calcularFit;
})(this);
