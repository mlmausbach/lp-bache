/* O bache.com.br é um Worker com assets (Workers Builds publica o master).
 *
 * O site inteiro é estático e o Cloudflare serve os arquivos antes de chegar
 * aqui: este código só roda quando o caminho não é um arquivo. Hoje isso é
 * /api/lead, o pedido de Raio-X do formulário. O resto volta para os assets,
 * que respondem 404 quando o arquivo não existe.
 */

import { lead } from './lead.js';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/api/lead') return lead(request, env);
    return env.ASSETS.fetch(request);
  },
};
