# Método Protagonista — Seção interativa (tela dividida)

Data: 2026-06-13 · Status: aprovado (layout + copy validados em protótipo)

## Objetivo
Substituir a timeline vertical do `#metodo` por uma seção **interativa de tela dividida**: visão macro das 6 fases num trilho à esquerda; ao selecionar uma fase, o painel à direita destrincha o detalhe. Mais "sexy", clara e vendável; mobile-first.

## Decisões
- **Nome**: Método Protagonista™ (canônico). A imagem `metodo-protagonista-bache-framework.png` (rotulada "Dirige") não é usada; framework é reconstruído em HTML.
- **Arranjo**: Opção A — *espinha numerada* (trilho vertical 1→6 + painel de detalhe). Descartados hexágono/órbita (ordem de leitura ambígua, pior mobile) e stepper (pouco distintivo).
- **Acento**: `--ouro #C9A86A` (paleta sóbria já vigente), violeta `#7B35CE` como secundário. NÃO usar o teal dos tokens.
- **Copy**: alinhada ao `metodo-protagonista-bache.md` (regra de ouro: 4–5 linhas/fase, língua do paciente). Sem travessões (—); construção variada (ver memória feedback-copy-sem-travessao).

## Estrutura por fase (espinha de mecanismo do md)
Tag · Título · Virada (pull-quote) · Por que resolve · O que você recebe (bullets) · O sinal de que funcionou · (Fase 3: moat).

## Componentes
- `.metodo-explorer` — grid `300px | 1fr` (desktop).
- `.metodo-rail` (role=tablist) — 6 `.mx-tab` (role=tab): número, ícone, nome, tag.
- `.metodo-stage` — 6 `.mx-panel` (role=tabpanel); só o ativo visível; barra de progresso violeta→ouro no topo; contador `NN / 06`.
- Mantém-se: header (kicker/título/tese), `.metodo-rigor`, `.metodo-loops` (2 loops), `.metodo-bridge` (CTA). Removem-se os caps "Hoje…/Protagonista…" da metáfora linear.

## Interação / Acessibilidade
- Clique troca de fase; padrão ARIA tabs com roving tabindex (setas ←/→/↑/↓, Home/End).
- `prefers-reduced-motion`: sem animação de fade.
- Conteúdo injetado por JS a partir de um array `P` (fonte única; espelha o protótipo aprovado).

## Mobile (≤980px) — acordeão
- Vira **acordeão vertical** (decisão após comparar chips × acordeão × carrossel; chips reprovado por esconder fases 4–6 atrás de scroll horizontal).
- Cada fase = linha numerada (número + nome + tag + chevron); toca → expande o detalhe inline e fecha as outras (radio, sempre uma aberta). Scroll vertical só, zero scroll horizontal.
- Mesmo estado (`sel`) e mesmo conteúdo do desktop. JS renderiza `is-split` (desktop) ou `is-accordion` (mobile) conforme `matchMedia('(max-width: 980px)')`, e re-renderiza ao cruzar o breakpoint preservando a fase selecionada. Listeners por delegação no container (sobrevivem ao re-render). Barra de progresso e contador ocultos no acordeão.

## Framework macro (imagem que condensa o método)
- No topo da seção (após header/rigor, antes do explorer): **ring SVG** das 6 fases ao redor do centro "Método Protagonista™ · 6 fases · 1 ciclo", anel tracejado do ciclo, ícones por fase, acento ouro.
- Reconstruído em SVG (não o PNG `...-framework.png`, que tem fundo claro e diz "DIRIGE" — conflita com Protagonista e destoa do tema escuro).
- **Clicável**: tocar uma fase no ring chama `activate(i)` do explorer e rola até ele (`scroll-margin-top: 100px`). Nós com `role=button`, `tabindex=0`, Enter/Espaço.
- **Responsivo** (`renderFw(compact)`, rebuild no mesmo breakpoint do explorer): desktop = viewBox 640×470 com rótulos laterais (FASE N + nome); mobile = **modo compacto** viewBox 320×320 quadrado, sem rótulos laterais, nós grandes (~68px de alvo de toque) com ícone + número, centro "Método Protagonista™". Os nomes no mobile ficam no acordeão logo abaixo. (Motivo: o viewBox largo escalava a ~0.5 no celular, deixando texto ~6px ilegível.)

## Fora de escopo
Sem autoplay, sem alterar planos/comparativo/CTAs. PNG do framework não é usado (substituído pelo SVG).
