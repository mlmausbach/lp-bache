# Reestruturação de Método e Oferta — Bäche — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Método Protagonista (6-phase wheel) and the 4 priced tiers on `index.html` with a 4-frentes map + flywheel + entregáveis explorer, a 90-day motor, and 3 no-price plans, per `docs/superpowers/specs/2026-07-06-metodo-oferta-design.md`.

**Architecture:** Single-file static site (`index.html`, ~6300 lines, no build step, no test framework). Every task edits this one file directly with the `Edit` tool, using distinctive anchor strings (section ids, exact current text) rather than line numbers, because earlier tasks shift line numbers for everything below them. Interactive pieces (the ring diagram + explorer) are JS-rendered from a data array, following the codebase's existing convention — not rewritten as static HTML.

**Tech Stack:** Vanilla HTML/CSS/JS, no framework, no package manager, no bundler. Dev server: `npx serve -p 3000 .`.

## Global Constraints

- Visual identity (palette, fonts, grid, spacing, existing CSS classes) stays untouched. Only content, and the minimum new CSS/JS needed to render it, changes.
- No em dash (—) in any new copy. Vary sentence construction instead.
- Apply the glossário: never write CAC, LTV, funil de conversão, playbook/roadmap/sprint, growth, ROI in client-facing copy. Use custo por paciente, quanto o paciente vale ao longo do tempo, jornada do paciente, protocolo/plano de tratamento/etapa, diagnóstico/tratamento/retorno.
- Every new pain-opening line must match the table in the spec's "Padrão de copy" section (médico vs. clínica pains/gains/JTBD) — don't write generic marketing copy.
- No R$ value may describe a Bäche plan/tier anywhere, including JSON-LD. The only allowed R$ mentions after this plan: the FAQ's hypothetical-competitor price (`R$2.000/mês`, task 9) and the qualification modal's revenue brackets describing the client's own business (untouched, out of scope).
- All existing section `id` attributes are preserved (`#hero`, `#stats`, `#dor`, `#guia`, `#metodo`, `#plano`, `#diferenciais`, `#transformacao`, `#produtos`, `#garantia`, `#fundadores`, `#faq`, `#contato`) so nav anchors and analytics events keep working.
- Before any Edit on a section this plan didn't fully quote verbatim, re-read the current exact block first (`Read` with the given line hint) and confirm the anchor text still matches — line numbers drift as earlier tasks land.
- Commit after every task, scoped to that task's change only.

---

### Task 1: JSON-LD — replace old offer catalog

**Files:**
- Modify: `index.html` (head, `<script type="application/ld+json">` block, currently lines 61-209 — re-read lines 119-153 to confirm exact bounds before editing)

**Interfaces:**
- Consumes: nothing (first task, no dependency on other tasks)
- Produces: nothing later tasks depend on programmatically (this is structured data, not code other tasks call)

- [ ] **Step 1: Re-confirm current exact block**

Run: read `index.html` lines 119-153. Confirm it still starts with `"@type": "ProfessionalService",` and the `hasOfferCatalog.itemListElement` array still has exactly 4 offers named `Diagnóstico Bäche`, `Sprint Ignição`, `Retainer Presença`, `Programa Palco`. If it differs, stop and re-read a wider range before proceeding.

- [ ] **Step 2: Replace the itemListElement array**

Old string (inside the `hasOfferCatalog` object):

```json
          "itemListElement": [
            {
              "@type": "Offer",
              "name": "Diagnóstico Bäche",
              "description": "Sessão única de 2 horas para análise completa da presença digital e posicionamento do especialista médico. Inclui mapa de oportunidades e plano de ação.",
              "price": "0",
              "priceCurrency": "BRL"
            },
            {
              "@type": "Offer",
              "name": "Sprint Ignição",
              "description": "Projeto de 30 dias para construção das bases de autoridade de marca do especialista médico, incluindo brand audit, arquétipo, posicionamento e 1 dia de gravação com direção cênica."
            },
            {
              "@type": "Offer",
              "name": "Retainer Presença",
              "description": "Gestão mensal completa de presença e performance para médicos e clínicas, com direção cênica mensal, tráfego pago, dashboard de resultados e treinamento de equipe comercial. Inclui garantia de resultado em 90 dias."
            },
            {
              "@type": "Offer",
              "name": "Programa Palco",
              "description": "Programa completo de dominância de mercado para especialistas e clínicas, incluindo rebrand, estratégia multi-canal, vídeo institucional e evento de lançamento."
            }
          ]
```

New string:

```json
          "itemListElement": [
            {
              "@type": "Offer",
              "name": "Raio-X Bäche",
              "description": "Diagnóstico comercial gratuito de 2 horas por call. Sai com nota por frente de crescimento e o vazamento de receita mais óbvio apontado.",
              "price": "0",
              "priceCurrency": "BRL"
            },
            {
              "@type": "Offer",
              "name": "Essencial",
              "description": "Para clínicas começando a estruturar marketing: 2 a 3 frentes de crescimento priorizadas no Raio-X, painel único e reuniões quinzenais, foco no vazamento de receita mais óbvio."
            },
            {
              "@type": "Offer",
              "name": "Ciclo completo",
              "description": "As 4 frentes de crescimento (marca, aquisição, conversão, retenção), painel único, reuniões quinzenais, gravação de conteúdo em lote mensal com edição e postagem pela Bäche."
            },
            {
              "@type": "Offer",
              "name": "Rede",
              "description": "As 4 frentes de crescimento replicadas por unidade, para clínicas com mais de uma unidade ou vários médicos. Relatório consolidado e governança de marca entre unidades."
            }
          ]
```

- [ ] **Step 3: Validate JSON syntax**

Run: `node -e "JSON.parse(require('fs').readFileSync('index.html','utf8').match(/<script type=\"application\/ld\+json\">([\s\S]*?)<\/script>/)[1])"`
Expected: no output, exit code 0 (valid JSON). If it throws, fix the syntax error before continuing.

- [ ] **Step 4: Grep-verify old names are gone from this block**

Run: `grep -c "Sprint Ignição\|Retainer Presença\|Programa Palco" index.html`
Expected: count reflects only remaining mentions elsewhere in the file (handled by later tasks) — this count should drop after this step compared to before it. Don't expect 0 yet; Tasks 4, 7, 10 remove the rest.

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "feat(schema): JSON-LD oferta reflete Raio-X + 3 planos, sem tiers antigos"
```

---

### Task 2: Stats + dor — round false-precision numbers, add opening line

**Files:**
- Modify: `index.html` (`#stats`, currently lines 4258-4280; `#dor` opening, currently lines 4285-4292)

**Interfaces:**
- Consumes: nothing
- Produces: nothing later tasks depend on

- [ ] **Step 1: Replace the 3 stat tiles**

Old string:

```html
      <div class="stat-item" data-transition="spring" data-state="entering" data-duration="normal" aria-label="291.362 clínicas disputando o mesmo paciente particular">
        <div class="stat-number" aria-hidden="true">
          <span class="counter" data-target="291362" data-format="number">291.362</span>
        </div>
        <div class="stat-label" aria-hidden="true">Clínicas disputando<br/>o mesmo paciente particular</div>
      </div>
      <div class="stat-item" data-transition="spring" data-state="entering" data-duration="normal" data-delay="2" aria-label="41% das clínicas sem nenhuma estratégia de diferenciação">
        <div class="stat-number" aria-hidden="true">
          <span class="counter" data-target="41" data-format="percent">41</span><span class="stat-accent">%</span>
        </div>
        <div class="stat-label" aria-hidden="true">Sem nenhuma estratégia<br/>de diferenciação</div>
      </div>
      <div class="stat-item" data-transition="spring" data-state="entering" data-duration="normal" data-delay="4" aria-label="Apenas 25% com marketing que gera pacientes de verdade">
        <div class="stat-number" aria-hidden="true">
          <span class="counter" data-target="25" data-format="percent">25</span><span class="stat-accent">%</span>
        </div>
        <div class="stat-label" aria-hidden="true">Com marketing que<br/>gera pacientes de verdade</div>
      </div>
```

New string:

```html
      <div class="stat-item" data-transition="spring" data-state="entering" data-duration="normal" aria-label="Centenas de milhares de clínicas disputando o mesmo paciente particular">
        <div class="stat-number" aria-hidden="true">Centenas de milhares</div>
        <div class="stat-label" aria-hidden="true">De clínicas disputando<br/>o mesmo paciente particular</div>
      </div>
      <div class="stat-item" data-transition="spring" data-state="entering" data-duration="normal" data-delay="2" aria-label="Boa parte das clínicas sem nenhuma estratégia de diferenciação">
        <div class="stat-number" aria-hidden="true">Boa parte</div>
        <div class="stat-label" aria-hidden="true">Das clínicas sem nenhuma<br/>estratégia de diferenciação</div>
      </div>
      <div class="stat-item" data-transition="spring" data-state="entering" data-duration="normal" data-delay="4" aria-label="Uma minoria com marketing que gera pacientes de verdade">
        <div class="stat-number" aria-hidden="true">Uma minoria</div>
        <div class="stat-label" aria-hidden="true">Com marketing que<br/>gera pacientes de verdade</div>
      </div>
```

Note: this removes every `.counter`/`data-target` span. The counter-animation JS (`animateCounter`, `counterObserver`, later in the file) stays untouched — `document.querySelectorAll('.counter')` will simply match nothing, which is harmless. Don't touch that JS in this task.

- [ ] **Step 2: Add the vilão opening line to `#dor`**

Old string:

```html
      <div class="dor-left">
        <div class="section-label reveal">Por que o marketing médico não funciona</div>
        <h2 class="section-title">Você investe em ads.<br/><em>O custo de cada paciente</em><br/>não para de subir.</h2>
```

New string:

```html
      <div class="dor-left">
        <div class="section-label reveal">Por que o marketing médico não funciona</div>
        <p class="reveal" style="font-family:var(--font-headline);font-weight:800;font-size:clamp(20px,3vw,28px);color:var(--nevoa);margin:0 0 20px;letter-spacing:-0.01em;">Pare de decidir seu marketing no escuro.</p>
        <h2 class="section-title">Você investe em ads.<br/><em>O custo de cada paciente</em><br/>não para de subir.</h2>
```

- [ ] **Step 3: Verify**

Run: `grep -n "291.362\|data-target=\"41\"\|data-target=\"25\"" index.html`
Expected: no output (all 3 removed).

Run: `grep -n "Pare de decidir seu marketing no escuro" index.html`
Expected: 1 match.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "fix(credibilidade): estatisticas sem falsa precisao, abre dor com o vilao"
```

---

### Task 3: `#metodo` — mapa de 4 frentes + flywheel + entregáveis explorer

This is the largest task: it replaces the 6-phase Método Protagonista (wrapper HTML + `P` data array + ring/explorer JS engine) with the 4-frentes model. Read the spec's Decision A before starting if anything below is unclear.

**Files:**
- Modify: `index.html`:
  - Wrapper HTML: `<section id="metodo">`, currently lines 4415-4478 (re-read to confirm current bounds — ends right before the `<!-- PLANO -->` comment / `<section id="plano"`)
  - JS engine: the IIFE currently at lines 5178-5418 (`// ---- Método Protagonista: explorador interativo das 6 fases ----` through its closing `})();`)
  - Footer nav label: line ~5046 `<li><a href="#metodo">O Método Protagonista</a></li>` — **do not touch in this task**, it's handled in Task 10 alongside the rest of the footer.

**Interfaces:**
- Consumes: nothing from other tasks
- Produces: the `FRENTES` array (replaces `P`), indices `0=Marca (hub), 1=Aquisição, 2=Conversão, 3=Retenção`; the `.resp-badge` / `.resp-badge.faz` / `.resp-badge.dirige` / `.resp-badge.opera` CSS classes (no other task uses these, but keep the names if you touch this area again later)

- [ ] **Step 1: Re-confirm current exact bounds**

Read `index.html` lines 4415-4485 and lines 5178-5420. Confirm the section still opens with `<section id="metodo" aria-label="O Método Protagonista">` and the script IIFE still opens with `// ---- Método Protagonista: explorador interativo das 6 fases ----`. If line numbers shifted (Tasks 1-2 add/remove a few lines), search for these exact strings instead of trusting the numbers.

- [ ] **Step 2: Replace the wrapper HTML**

Old string (from `<section id="metodo"` through the closing `</section>` right before `<!-- ======================================== \n       PLANO`) — locate via the section's known content; the block contains `Método Protagonista™`, `.metodo-tese`, `.metodo-rigor`, `.metodo-fw`/`#metodoFw`, `#metodoExplorer`, `.metodo-loops` (2 cards: "Loop de aprendizado" / "Loop econômico"), and `.metodo-bridge` with 2 CTAs. Replace that entire block with:

```html
  <section id="metodo" aria-label="Como fazemos sua clínica crescer">
    <div class="metodo-inner">
      <div class="metodo-header">
        <div class="reveal">
          <div class="section-label">Como fazemos sua clínica crescer</div>
          <h2 class="section-title">Não é mais um funil.<br/>É uma <em>roda</em> que gira em torno da sua marca.</h2>
        </div>
        <p class="metodo-tese reveal reveal-delay-1">
          O paciente não escolhe o médico mais competente, porque não tem como avaliar competência técnica. Ele escolhe o médico que <strong>entende, lembra e confia</strong>. Marca é o eixo. Aquisição, conversão e retenção giram em torno dela, e cada volta fica mais barata que a anterior.
        </p>
        <div class="metodo-rigor reveal reveal-delay-2">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.29 1.51 4.04 3 5.5l7 7Z"/></svg>
          <span><strong>Rigor clínico.</strong> Nenhum médico prescreve sem examinar, mas é exatamente isso que o mercado faz com você quando vende post e tráfego sem diagnóstico. Aqui, seu crescimento é tratado com o mesmo rigor que você aplica aos seus pacientes.</span>
        </div>
      </div>

      <figure class="metodo-fw">
        <div class="mfw-stage" id="metodoFw" role="img" aria-label="O mapa de 4 frentes girando em torno da marca"></div>
        <figcaption>No primeiro ciclo a roda gira com atrito alto: pouca prova, marca ainda jovem. A cada retorno bem-sucedido, o reconhecimento cresce e a volta seguinte exige menos mídia pelo mesmo resultado. <strong>Clique numa frente</strong> para abrir o detalhe abaixo.</figcaption>
      </figure>

      <div class="metodo-explorer" id="metodoExplorer" aria-label="As 4 frentes de crescimento"></div>

      <div class="metodo-incluso reveal">
        <div class="section-label" style="margin-bottom:10px;">Incluído em todo plano</div>
        <ul class="mx-list">
          <li><span class="resp-badge faz">Bäche faz</span> Painel único: custo por paciente, valor no tempo, ocupação, margem</li>
          <li><span class="resp-badge faz">Bäche faz</span> Reunião quinzenal de leitura dos números, com você na sala</li>
        </ul>
        <p style="margin-top:10px;font-size:13px;color:var(--text-secondary);">Nunca é uma frente. É a régua que mede as quatro.</p>
      </div>

      <div class="metodo-bridge reveal">
        <p class="metodo-bridge-text">O mapa mostra onde mexemos.<br/><em>O motor, na próxima seção, mostra como.</em></p>
        <div class="metodo-bridge-actions">
          <a href="#contato" class="btn-primary" data-modal="diagnostico">
            Agendar meu Raio-X gratuito
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </a>
          <a href="#produtos" class="btn-ghost">Conhecer os planos</a>
        </div>
      </div>
    </div>
  </section>

  <style>
    .resp-badge{display:inline-block;padding:3px 9px;border-radius:100px;font-size:9.5px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;white-space:nowrap;margin-right:8px;vertical-align:1px;}
    .resp-badge.faz{background:rgba(123,53,206,0.20);color:var(--violeta-light);border:1px solid rgba(123,53,206,0.30);}
    .resp-badge.dirige{background:rgba(201,168,106,0.14);color:var(--ouro);border:1px solid rgba(201,168,106,0.30);}
    .resp-badge.opera{background:rgba(255,255,255,0.06);color:rgba(232,230,245,0.65);border:1px solid rgba(255,255,255,0.14);}
  </style>
```

This drops `.metodo-loops` entirely (no replacement needed — see spec's Decision A rationale) and reuses `.metodo-inner`, `.metodo-header`, `.metodo-tese`, `.metodo-rigor`, `.metodo-fw`/`#metodoFw`, `#metodoExplorer`, `.metodo-bridge`/`.metodo-bridge-text` classes as-is (same CSS applies, only text changed). `.metodo-incluso` is a new wrapper class with no CSS rule of its own — it inherits section spacing from `.metodo-inner`'s existing child margins; if it renders flush against neighboring blocks, add `style="margin-top:40px;"` inline during the visual QA pass (Step 8). The `<style>` block right after `</section>` follows the same co-location convention already used for the qualification modal's styles elsewhere in the file.

- [ ] **Step 3: Replace the `P` array and icon set with `FRENTES`**

Old string:

```javascript
      const ICONS = [
        '<path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6 6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3"/><path d="M8 15v1a6 6 0 0 0 6 6 6 6 0 0 0 6-6v-4"/><circle cx="20" cy="10" r="2"/>',
        '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88"/>',
        '<path d="M20.2 6 3 11l-.9-2.4c-.3-1.1.3-2.2 1.3-2.5l13.5-4c1.1-.3 2.2.3 2.5 1.3Z"/><path d="m6.2 5.3 3.1 3.9"/><path d="m12.4 3.4 3.1 4"/><path d="M3 11h18v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/>',
        '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
        '<path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/>',
        '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>'
      ];
      const P = [
        { n: 'Diagnóstico', tag: 'Gratuito · 2h · via call', title: 'Diagnóstico Bäche',
          virada: '"Paro de adivinhar. Sei exatamente onde minha agenda particular trava."',
          why: 'Sem diagnóstico, toda ação vira tiro no escuro. Primeiro a gente descobre por onde sua receita vaza (posicionamento, percepção, aquisição ou conversão) pra que o próximo passo seja mirado, não chutado.',
          recebe: ['<strong>Auditoria completa</strong> da sua presença digital: o retrato real de como o paciente te encontra hoje.', '<strong>Auditoria de indicadores</strong> com ROI, CAC, LTV, ticket médio e churn, a foto financeira de onde você está.', '<strong>Diagnóstico de posicionamento</strong> que cruza você, a concorrência e o que o paciente de fato procura.', 'Um <strong>brand diagnosis</strong> que aponta o que te torna único e, principalmente, vendável.', '<strong>Plano de ação de 30 dias</strong> que fica com você, mesmo se não seguir com a gente.'],
          sinal: 'Você termina a call sabendo nomear sua trava nº 1 e os três próximos movimentos concretos.' },
        { n: 'Marca & Mensagem', tag: 'Base de autoridade', title: 'Marca & Mensagem',
          virada: '"Paro de soar como todo mundo. Ocupo um lugar que é só meu."',
          why: 'Quando todo perfil repete as mesmas palavras (humanização, excelência, cuidado), sobra um único critério de escolha: o preço. Aqui a gente traduz o que te torna único para a língua do paciente, sempre dentro do CFM.',
          recebe: ['<strong>Persona de autoridade</strong>: quem você é para o mercado, numa identidade que o paciente reconhece e confia.', '<strong>Inimigo comum</strong>, porque todo posicionamento forte precisa de um adversário claro.', '<strong>Narrativa central e mensagens-chave</strong> na língua do paciente, 100% CFM-safe.', '<strong>Oferta e público de alto valor</strong> definidos antes de qualquer anúncio rodar.'],
          sinal: 'Um estranho lê seu posicionamento e resume, numa frase, por que escolher você. Sem falar em preço.' },
        { n: 'Direção Cênica', tag: 'O diferencial incopiável', title: 'Direção Cênica & Produção',
          virada: '"Paro de travar na câmera. Transmito a autoridade que já tenho."',
          why: 'Autoridade percebida não vem do quanto você sabe, e sim de como você comunica. Direção cênica vem do palco: técnica de voz, postura e ritmo que revelam o comunicador que já existe em você. É o motor de conversão do método inteiro, não um conforto opcional.',
          recebe: ['<strong>Roteiros dirigidos por tema</strong> que você conduz em vez de decorar.', '<strong>Frameworks e templates de conteúdo</strong> desenhados para o seu nicho.', '<strong>Um dia de gravação dirigida</strong> (cerca de 6h) que rende 15 a 20 peças, um mês inteiro de presença.', '<strong>Direção de câmera, postura e fala</strong> em tempo real, com a gente do seu lado.', '<strong>Edição e calendário de publicação</strong> prontos. Depois de gravar, você não toca em mais nada.'],
          sinal: 'Você se assiste sem vergonha do resultado e fecha o mês inteiro de conteúdo num único dia.',
          moat: '<strong>Por que ninguém copia:</strong> agência tem social media. A Bäche tem direção cênica de verdade, anos de palco aplicados à câmera. Isso não se compra com ferramenta. Ou você é diretor, ou não é.' },
        { n: 'Aquisição', tag: 'Presença que converte', title: 'Aquisição',
          virada: '"Paro de pagar pra falar com estranho. Sou achado por quem já me conhece."',
          why: 'Anúncio para estranho é leilão de preço. Anúncio sobre a marca que você construiu nas fases anteriores chega em quem já te reconhece, e quem reconhece não compara: agenda. No topo, o Meta cria a demanda. No fundo, o Google colhe quem já procura por você.',
          recebe: ['<strong>Campanhas no Meta e no Google Busca</strong>, com setup, gestão e Google Meu Negócio na sequência.', '<strong>Criativos tirados das suas gravações</strong>, nada de banco de imagem genérico.', '<strong>Landing pages por estágio de consciência</strong>, do curioso ao paciente pronto pra agendar.', '<strong>Assessoria de imprensa</strong> que coloca terceiros confirmando você quando buscam seu nome.', '<strong>Otimização por custo por paciente</strong> e retorno sobre a mídia, não por clique e muito menos por curtida.'],
          sinal: 'Seu custo por paciente cai mês a mês, e os leads começam a chegar dizendo "já te acompanho".' },
        { n: 'Conversão', tag: 'O contato vira paciente', title: 'Conversão & Mensuração',
          virada: '"Paro de torcer. Vejo cada real virar paciente, em tempo real."',
          why: 'O gargalo quase nunca está na mídia. Ele está no último metro, o lead que morre no WhatsApp, e na falta de dados pra enxergar isso. A gente treina sua equipe pra converter e instala o painel que mostra exatamente onde cada paciente se perde.',
          recebe: ['<strong>Treinamento comercial e scripts de atendimento</strong> que transformam a secretária em parte da estratégia.', '<strong>Resposta em menos de 5 minutos</strong>, com processo claro de atendimento e agendamento.', '<strong>Dashboard em tempo real</strong> com pacientes por canal, ticket médio e taxa de conversão.', '<strong>CRM oficial Bäche®</strong> que acompanha o SLA de atendimento e os KPIs da clínica.', '<strong>Baseline no dia zero e relatório quinzenal</strong>, mais garantia condicional de 90 dias.'],
          sinal: 'Você abre o painel e sabe, sem perguntar a ninguém, quantos pacientes vieram, de qual canal e a que custo. Resposta ao lead em menos de 5 minutos e taxa de agendamento acima de 40%.' },
        { n: 'Fidelização', tag: 'O paciente vira defensor', title: 'Fidelização',
          virada: '"Paro de recomeçar do zero. Colho a base que já conquistei."',
          why: 'O paciente mais barato é o que você já tem. Quem volta sustenta a receita, quem indica derruba seu custo de captação e quem avalia vira prova social que realimenta o tráfego. No fim, o método inteiro fica mais barato a cada mês.',
          recebe: ['<strong>Régua de relacionamento pós-consulta</strong> com lembretes, conteúdo e reativação de base parada.', '<strong>Geração ativa de avaliações</strong> no Google e na Doctoralia, que viram combustível do topo de funil.', '<strong>Indicação em duas frentes</strong>: pacientes que indicam pacientes e a rede de encaminhamento profissional, sempre sem comissão (vedado pelo CFM).', '<strong>Conteúdo de nutrição</strong> pra quem já te segue continuar lembrando de você.'],
          sinal: 'As indicações sobem, as avaliações 5★ crescem e seu custo de captação cai, porque agora a base trabalha por você.' }
      ];
```

New string:

```javascript
      const ICONS = [
        '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88"/>',
        '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
        '<path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/>',
        '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>'
      ];
      const TIER_LABEL = { faz: 'Bäche faz', dirige: 'Bäche dirige', opera: 'Sua equipe opera' };
      const FRENTES = [
        { n: 'Marca', tag: 'Por que escolhem você', title: 'Marca',
          virada: '"Aceita convênio?" costuma ser a primeira pergunta, antes do paciente saber o que te torna diferente de qualquer outro especialista da cidade.',
          why: 'Marca é o que muda a ordem dessa pergunta: ela vem depois da decisão de te escolher, não antes.',
          recebe: [
            { txt: 'Posicionamento e mensagem central da clínica', tier: 'faz' },
            { txt: 'Análise de concorrentes e leitura de mercado', tier: 'faz' },
            { txt: 'Tom de voz e linha editorial próprios', tier: 'faz' }
          ],
          conteudo: [
            { txt: 'Pauta, roteiro e direção editorial do mês', tier: 'faz' },
            { txt: 'Treino de câmera do médico', tier: 'faz' },
            { txt: 'Gravação, edição e postagem, produzidas pela operação Bäche', tier: 'faz' }
          ],
          sinal: 'Um estranho lê seu posicionamento e sabe, numa frase, por que te escolher, sem mencionar preço.' },
        { n: 'Aquisição', tag: 'O paciente certo chega', title: 'Aquisição',
          virada: 'Você paga pra aparecer, e quem chega é curioso, caçador de desconto ou ninguém.',
          why: 'Sem marca por trás, todo anúncio vira leilão de preço. Aquisição bem feita alcança quem já reconhece você, e esse não compara: agenda.',
          recebe: [
            { txt: 'Estratégia e gestão de tráfego pago (Google e Meta)', tier: 'faz' },
            { txt: 'Criativos de anúncio: conceito, copy e arte', tier: 'faz' },
            { txt: 'Parcerias e eventos que encaminham pacientes', tier: 'dirige' }
          ],
          sinal: 'Custo por paciente caindo mês a mês, porque a marca faz o anúncio trabalhar menos.' },
        { n: 'Conversão', tag: 'O contato vira paciente', title: 'Conversão',
          virada: 'O lead chega no WhatsApp, a secretária demora, informa preço, não agenda.',
          why: 'O gargalo raramente é a mídia, é o último metro. Conversão instala processo e painel pra fechar essa brecha antes que o paciente esfrie.',
          recebe: [
            { txt: 'Landing pages e páginas de conversão', tier: 'faz' },
            { txt: 'CRM com WhatsApp e agenda: escolha, setup e automações', tier: 'faz' },
            { txt: 'Script comercial e treinamento da secretária', tier: 'faz' },
            { txt: 'Régua contra faltas e recuperação de orçamentos parados', tier: 'faz' },
            { txt: 'Atendimento diário no CRM e no WhatsApp', tier: 'opera' }
          ],
          sinal: 'Resposta ao paciente em minutos, não horas, e a secretária virou parte do crescimento, não um gargalo.' },
        { n: 'Retenção', tag: 'O paciente volta e indica', title: 'Retenção',
          virada: 'Você paga caro pra trazer o paciente, ele é bem atendido, e some.',
          why: 'O paciente mais barato é o que você já tem. Retenção transforma quem já veio em quem indica o próximo, derrubando o custo do ciclo seguinte.',
          recebe: [
            { txt: 'Régua de pós-consulta e follow-up automatizado', tier: 'faz' },
            { txt: 'Motor de indicação e avaliações públicas', tier: 'faz' },
            { txt: 'Campanha de reativação da base parada', tier: 'faz' }
          ],
          sinal: 'Percentual de pacientes por indicação subindo, e o custo por paciente caindo porque a base trabalha por você.' }
      ];
```

- [ ] **Step 4: Replace `tabMarkup`/`panelMarkup` to render tags and the Conteúdo sub-block**

Old string:

```javascript
      function tabMarkup(p, i) {
        return '<button type="button" class="mx-tab" data-i="' + i + '" id="mx-tab-' + i + '" aria-controls="mx-panel-' + i + '" aria-expanded="false">' +
          '<span class="mx-tab-num">' + NN(i) + '</span>' +
          '<span class="mx-tab-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICONS[i] + '</svg></span>' +
          '<span class="mx-tab-tx"><span class="mx-tab-name">' + p.n + '</span><span class="mx-tab-tag">' + p.tag + '</span></span>' +
          '<span class="mx-chev" aria-hidden="true"><svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg></span>' +
          '</button>';
      }
      function panelMarkup(p, i) {
        return '<div class="mx-panel" data-i="' + i + '" id="mx-panel-' + i + '" role="region" aria-labelledby="mx-tab-' + i + '" hidden>' +
          '<div class="mx-bar" style="width:' + ((i + 1) / P.length * 100) + '%"></div>' +
          '<div class="mx-count">' + NN(i) + ' / 06</div>' +
          '<div class="mx-tag">' + p.tag + '</div>' +
          '<h3 class="mx-title">' + p.title + '</h3>' +
          '<p class="mx-virada">' + p.virada + '</p>' +
          '<p class="mx-why">' + p.why + '</p>' +
          '<div class="mx-recebe-label">O que você recebe</div>' +
          '<ul class="mx-list">' + p.recebe.map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ul>' +
          '<div class="mx-sinal"><strong>O sinal de que funcionou</strong>' + p.sinal + '</div>' +
          (p.moat ? '<div class="mx-moat">' + p.moat + '</div>' : '') +
          '</div>';
      }
```

New string:

```javascript
      function tabMarkup(p, i) {
        return '<button type="button" class="mx-tab" data-i="' + i + '" id="mx-tab-' + i + '" aria-controls="mx-panel-' + i + '" aria-expanded="false">' +
          '<span class="mx-tab-num">' + NN(i) + '</span>' +
          '<span class="mx-tab-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICONS[i] + '</svg></span>' +
          '<span class="mx-tab-tx"><span class="mx-tab-name">' + p.n + '</span><span class="mx-tab-tag">' + p.tag + '</span></span>' +
          '<span class="mx-chev" aria-hidden="true"><svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg></span>' +
          '</button>';
      }
      function recebeItem(x) {
        return '<li><span class="resp-badge ' + x.tier + '">' + TIER_LABEL[x.tier] + '</span>' + x.txt + '</li>';
      }
      function panelMarkup(p, i) {
        return '<div class="mx-panel" data-i="' + i + '" id="mx-panel-' + i + '" role="region" aria-labelledby="mx-tab-' + i + '" hidden>' +
          '<div class="mx-bar" style="width:' + ((i + 1) / FRENTES.length * 100) + '%"></div>' +
          '<div class="mx-count">' + NN(i) + ' / ' + NN(FRENTES.length - 1) + '</div>' +
          '<div class="mx-tag">' + p.tag + '</div>' +
          '<h3 class="mx-title">' + p.title + '</h3>' +
          '<p class="mx-virada">' + p.virada + '</p>' +
          '<p class="mx-why">' + p.why + '</p>' +
          '<div class="mx-recebe-label">O que você recebe</div>' +
          '<ul class="mx-list">' + p.recebe.map(recebeItem).join('') + '</ul>' +
          (p.conteudo ? '<div class="mx-recebe-label">+ Conteúdo (incluso no Ciclo completo e na Rede)</div><ul class="mx-list">' + p.conteudo.map(recebeItem).join('') + '</ul>' : '') +
          '<div class="mx-sinal"><strong>O sinal de que funcionou</strong>' + p.sinal + '</div>' +
          '</div>';
      }
```

- [ ] **Step 5: Replace every remaining `P` reference with `FRENTES` in the same IIFE**

Run: `grep -n "\bP\b" index.html` restricted to this IIFE's line range and replace each remaining bare reference. The occurrences to fix (all within the same script block from Step 3-4's location onward):

- `render(accordion)` function: `explorer.innerHTML = P.map(...)` (2 occurrences: accordion branch and split branch) → `FRENTES.map(...)`
- `renderFw(compact)` function: `const N = P.map(function (p, i) { return at(i); });` → replaced entirely in Step 6 below (don't edit here, Step 6 supersedes this whole function)

For `render(accordion)`, old string:

```javascript
        if (accordion) {
          explorer.innerHTML = P.map(function (p, i) {
            return '<div class="mx-item" data-i="' + i + '">' + tabMarkup(p, i) + panelMarkup(p, i) + '</div>';
          }).join('');
        } else {
          explorer.innerHTML =
            '<div class="metodo-rail">' + P.map(tabMarkup).join('') + '</div>' +
            '<div class="metodo-stage">' + P.map(panelMarkup).join('') + '</div>';
        }
```

New string:

```javascript
        if (accordion) {
          explorer.innerHTML = FRENTES.map(function (p, i) {
            return '<div class="mx-item" data-i="' + i + '">' + tabMarkup(p, i) + panelMarkup(p, i) + '</div>';
          }).join('');
        } else {
          explorer.innerHTML =
            '<div class="metodo-rail">' + FRENTES.map(tabMarkup).join('') + '</div>' +
            '<div class="metodo-stage">' + FRENTES.map(panelMarkup).join('') + '</div>';
        }
```

- [ ] **Step 6: Replace `renderFw` — hub becomes Marca, 3 nodes orbit instead of 6**

Old string (the full `renderFw` function body plus its `at`/`N` setup, from `function renderFw(compact) {` through the closing `}` right before `function fitFw() {`):

```javascript
      function renderFw(compact) {
        if (!fw) return;
        const fig = fw.closest('.metodo-fw');
        if (fig) fig.classList.toggle('is-compact', compact);

        const NODE = compact ? 80 : 124, NR = NODE / 2;
        const R = compact ? 142 : 250, HUB_R = compact ? 66 : 122;
        const ICSZ = compact ? 28 : 34, BADGE = compact ? 28 : 36;
        const LBLW = 172, GAP = 20;

        let W, H, CX, CY;
        if (compact) {
          W = Math.ceil((R + NR) * 2 + 20); H = W; CX = W / 2; CY = H / 2;
        } else {
          const halfX = R * Math.cos(Math.PI / 6) + NR + GAP + LBLW;
          W = Math.ceil(halfX * 2); CX = W / 2;
          CY = R + NR + 18; H = Math.ceil(CY + R + NR + 78);
        }

        const at = function (i) { const a = (-90 + i * 60) * Math.PI / 180; return { i: i, x: CX + R * Math.cos(a), y: CY + R * Math.sin(a) }; };
        const N = P.map(function (p, i) { return at(i); });

        // wires (svg string)
        let sg = '<defs><marker id="fwArr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="rgba(232,230,245,0.42)"/></marker></defs>';
        sg += '<circle cx="' + CX + '" cy="' + CY + '" r="' + HUB_R + '" fill="rgba(123,53,206,0.06)" stroke="rgba(168,101,240,0.42)" stroke-width="1.2" stroke-dasharray="2 8" stroke-linecap="round"/>';
        N.forEach(function (nd) {
          var dx = nd.x - CX, dy = nd.y - CY, l = Math.hypot(dx, dy), ux = dx / l, uy = dy / l;
          var sx = CX + ux * (HUB_R + 10), sy = CY + uy * (HUB_R + 10), ex = nd.x - ux * (NR + 11), ey = nd.y - uy * (NR + 11);
          sg += '<line x1="' + sx.toFixed(1) + '" y1="' + sy.toFixed(1) + '" x2="' + ex.toFixed(1) + '" y2="' + ey.toFixed(1) + '" stroke="rgba(201,168,106,0.32)" stroke-width="1.2" stroke-dasharray="2 8" stroke-linecap="round"/>';
          sg += '<circle cx="' + ex.toFixed(1) + '" cy="' + ey.toFixed(1) + '" r="2.6" fill="rgba(201,168,106,0.85)"/>';
        });
        for (var k = 0; k < N.length; k++) {
          var a = N[k], b = N[(k + 1) % N.length];
          var dx2 = b.x - a.x, dy2 = b.y - a.y, l2 = Math.hypot(dx2, dy2), ux2 = dx2 / l2, uy2 = dy2 / l2;
          var sx2 = a.x + ux2 * (NR + 13), sy2 = a.y + uy2 * (NR + 13), ex2 = b.x - ux2 * (NR + 21), ey2 = b.y - uy2 * (NR + 21);
          sg += '<line x1="' + sx2.toFixed(1) + '" y1="' + sy2.toFixed(1) + '" x2="' + ex2.toFixed(1) + '" y2="' + ey2.toFixed(1) + '" stroke="rgba(232,230,245,0.34)" stroke-width="1.5" stroke-linecap="round" marker-end="url(#fwArr)"/>';
        }

        // nodes + labels (html string)
        var nodes = '';
        N.forEach(function (nd) {
          var i = nd.i;
          nodes += '<button type="button" class="fw-node" data-i="' + i + '" aria-label="Fase ' + (i + 1) + ': ' + P[i].n + '" ' +
            'style="left:' + nd.x + 'px;top:' + nd.y + 'px;width:' + NODE + 'px;height:' + NODE + 'px">' +
            '<span class="fw-badge" style="width:' + BADGE + 'px;height:' + BADGE + 'px;font-size:' + (compact ? 13 : 15) + 'px">' + NN(i) + '</span>' +
            '<span class="fw-ic"><svg width="' + ICSZ + '" height="' + ICSZ + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">' + ICONS[i] + '</svg></span>' +
            '</button>';
          if (!compact) {
            var cls, st;
            if (i === 3) { cls = 'center'; st = 'left:' + nd.x + 'px;top:' + (nd.y + NR + 16) + 'px;transform:translateX(-50%);width:240px'; }
            else if (nd.x >= CX) { cls = 'right'; st = 'left:' + (nd.x + NR + GAP) + 'px;top:' + nd.y + 'px;transform:translateY(-50%);width:' + LBLW + 'px'; }
            else { cls = 'left'; st = 'left:' + (nd.x - NR - GAP - LBLW) + 'px;top:' + nd.y + 'px;transform:translateY(-50%);width:' + LBLW + 'px'; }
            nodes += '<div class="fw-olabel ' + cls + '" style="' + st + '">' +
              '<div class="fw-fase">Fase ' + (i + 1) + '</div>' +
              '<div class="fw-name">' + P[i].n + '</div>' +
              '<div class="fw-desc">' + P[i].tag + '</div></div>';
          }
        });

        fw.innerHTML =
          '<div class="mfw-orb mfw-orb-v"></div><div class="mfw-orb mfw-orb-o"></div>' +
          '<div class="mfw-fit">' +
            '<div class="mfw-canvas" data-w="' + W + '" data-h="' + H + '" style="width:' + W + 'px;height:' + H + 'px">' +
              '<svg class="mfw-wires" viewBox="0 0 ' + W + ' ' + H + '" width="' + W + '" height="' + H + '">' + sg + '</svg>' +
              '<div class="mfw-diagram">' + nodes + '</div>' +
              '<div class="mfw-hub" style="left:' + CX + 'px;top:' + CY + 'px;width:' + (compact ? Math.round(HUB_R * 1.82) : 212) + 'px">' +
                '<div class="mfw-hub-title">MÉTODO<br>PROTAGONISTA</div>' +
                '<div class="mfw-hub-rule"></div>' +
                '<div class="mfw-hub-desc">A marca reduz o CAC. A performance traz pacientes agora. Juntas, compõem mês a mês.</div>' +
              '</div>' +
            '</div>' +
          '</div>';

        fw.querySelectorAll('.fw-node').forEach(function (b) {
          b.addEventListener('click', function () { select(+b.dataset.i, false); explorer.scrollIntoView({ behavior: 'smooth', block: 'start' }); });
        });
        fitFw();
      }
```

New string:

```javascript
      function renderFw(compact) {
        if (!fw) return;
        const fig = fw.closest('.metodo-fw');
        if (fig) fig.classList.toggle('is-compact', compact);

        const NODE = compact ? 80 : 124, NR = NODE / 2;
        const R = compact ? 142 : 250, HUB_R = compact ? 66 : 122;
        const ICSZ = compact ? 28 : 34, BADGE = compact ? 28 : 36;
        const LBLW = 172, GAP = 20;
        const HUB_SIZE = compact ? Math.round(HUB_R * 1.82) : 212;

        let W, H, CX, CY;
        if (compact) {
          W = Math.ceil((R + NR) * 2 + 20); H = W; CX = W / 2; CY = H / 2;
        } else {
          const halfX = R * Math.cos(Math.PI / 6) + NR + GAP + LBLW;
          W = Math.ceil(halfX * 2); CX = W / 2;
          CY = R + NR + 18; H = Math.ceil(CY + R + NR + 78);
        }

        // index 0 = Marca (hub, fixed at center). Indices 1-3 orbit at 120° apart, starting at top.
        const ORBIT = [1, 2, 3].map(function (i, k) {
          const a = (-90 + k * 120) * Math.PI / 180;
          return { i: i, x: CX + R * Math.cos(a), y: CY + R * Math.sin(a) };
        });

        // wires (svg string): dashed hub-to-node spokes + cycle arrows among the 3 orbiting nodes only
        let sg = '<defs><marker id="fwArr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="rgba(232,230,245,0.42)"/></marker></defs>';
        sg += '<circle cx="' + CX + '" cy="' + CY + '" r="' + HUB_R + '" fill="rgba(123,53,206,0.06)" stroke="rgba(168,101,240,0.42)" stroke-width="1.2" stroke-dasharray="2 8" stroke-linecap="round"/>';
        ORBIT.forEach(function (nd) {
          var dx = nd.x - CX, dy = nd.y - CY, l = Math.hypot(dx, dy), ux = dx / l, uy = dy / l;
          var sx = CX + ux * (HUB_R + 10), sy = CY + uy * (HUB_R + 10), ex = nd.x - ux * (NR + 11), ey = nd.y - uy * (NR + 11);
          sg += '<line x1="' + sx.toFixed(1) + '" y1="' + sy.toFixed(1) + '" x2="' + ex.toFixed(1) + '" y2="' + ey.toFixed(1) + '" stroke="rgba(201,168,106,0.32)" stroke-width="1.2" stroke-dasharray="2 8" stroke-linecap="round"/>';
          sg += '<circle cx="' + ex.toFixed(1) + '" cy="' + ey.toFixed(1) + '" r="2.6" fill="rgba(201,168,106,0.85)"/>';
        });
        for (var k = 0; k < ORBIT.length; k++) {
          var a = ORBIT[k], b = ORBIT[(k + 1) % ORBIT.length];
          var dx2 = b.x - a.x, dy2 = b.y - a.y, l2 = Math.hypot(dx2, dy2), ux2 = dx2 / l2, uy2 = dy2 / l2;
          var sx2 = a.x + ux2 * (NR + 13), sy2 = a.y + uy2 * (NR + 13), ex2 = b.x - ux2 * (NR + 21), ey2 = b.y - uy2 * (NR + 21);
          sg += '<line x1="' + sx2.toFixed(1) + '" y1="' + sy2.toFixed(1) + '" x2="' + ex2.toFixed(1) + '" y2="' + ey2.toFixed(1) + '" stroke="rgba(232,230,245,0.34)" stroke-width="1.5" stroke-linecap="round" marker-end="url(#fwArr)"/>';
        }

        // orbiting nodes + labels (html string)
        var nodes = '';
        ORBIT.forEach(function (nd) {
          var i = nd.i;
          nodes += '<button type="button" class="fw-node" data-i="' + i + '" aria-label="Frente: ' + FRENTES[i].n + '" ' +
            'style="left:' + nd.x + 'px;top:' + nd.y + 'px;width:' + NODE + 'px;height:' + NODE + 'px">' +
            '<span class="fw-badge" style="width:' + BADGE + 'px;height:' + BADGE + 'px;font-size:' + (compact ? 13 : 15) + 'px">' + NN(i) + '</span>' +
            '<span class="fw-ic"><svg width="' + ICSZ + '" height="' + ICSZ + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">' + ICONS[i] + '</svg></span>' +
            '</button>';
          if (!compact) {
            var cls, st;
            if (nd.x >= CX) { cls = 'right'; st = 'left:' + (nd.x + NR + GAP) + 'px;top:' + nd.y + 'px;transform:translateY(-50%);width:' + LBLW + 'px'; }
            else { cls = 'left'; st = 'left:' + (nd.x - NR - GAP - LBLW) + 'px;top:' + nd.y + 'px;transform:translateY(-50%);width:' + LBLW + 'px'; }
            nodes += '<div class="fw-olabel ' + cls + '" style="' + st + '">' +
              '<div class="fw-fase">' + FRENTES[i].tag + '</div>' +
              '<div class="fw-name">' + FRENTES[i].n + '</div></div>';
          }
        });

        // hub node (Marca) — same .fw-node class so click/active-state wiring below applies uniformly
        var hub = '<button type="button" class="fw-node mfw-hub" data-i="0" aria-label="Frente: Marca" ' +
          'style="left:' + CX + 'px;top:' + CY + 'px;width:' + HUB_SIZE + 'px;height:' + HUB_SIZE + 'px">' +
          '<div class="mfw-hub-title">MARCA</div>' +
          '<div class="mfw-hub-rule"></div>' +
          '<div class="mfw-hub-desc">O eixo. Aquisição, conversão e retenção giram em torno dela.</div>' +
          '</button>';

        fw.innerHTML =
          '<div class="mfw-orb mfw-orb-v"></div><div class="mfw-orb mfw-orb-o"></div>' +
          '<div class="mfw-fit">' +
            '<div class="mfw-canvas" data-w="' + W + '" data-h="' + H + '" style="width:' + W + 'px;height:' + H + 'px">' +
              '<svg class="mfw-wires" viewBox="0 0 ' + W + ' ' + H + '" width="' + W + '" height="' + H + '">' + sg + '</svg>' +
              '<div class="mfw-diagram">' + nodes + hub + '</div>' +
            '</div>' +
          '</div>';

        fw.querySelectorAll('.fw-node').forEach(function (b) {
          b.addEventListener('click', function () { select(+b.dataset.i, false); explorer.scrollIntoView({ behavior: 'smooth', block: 'start' }); });
        });
        fitFw();
      }
```

Note: `.mfw-hub` was previously a plain `<div>` positioned via inline `left`/`top`/`width` — it's now a `<button class="fw-node mfw-hub">`. `.fw-node` already resets button chrome (it was already rendered as a `<button>` for the orbit nodes before this change), so this should inherit clean styling; visually confirm in Step 8 that the hub still looks like a circular hub and not a default browser button. If `.mfw-hub`'s CSS assumes a `<div>` (e.g. a rule keyed to `div.mfw-hub`), broaden it to match any element, or add a small inline reset (`border:none;background:transparent;font:inherit;cursor:pointer;`) to the hub's style attribute.

- [ ] **Step 7: Update the two remaining comments and the accordion-count string for accuracy**

Old string:

```javascript
    // ---- Método Protagonista: explorador interativo das 6 fases ----
```

New string:

```javascript
    // ---- Mapa de frentes: explorador interativo (Marca/Aquisição/Conversão/Retenção) ----
```

Old string:

```javascript
      // ---- Framework macro (ring que condensa o método, clicável · compacto no mobile) ----
```

New string:

```javascript
      // ---- Flywheel (ring com Marca no hub, 3 frentes orbitando, clicável · compacto no mobile) ----
```

- [ ] **Step 8: Manual verification via dev server**

Run: `npx serve -p 3000 .` (background), then open `http://localhost:3000` in a browser.

Check:
1. The `#metodo` section shows a ring with a center hub labeled "MARCA" and 3 smaller nodes around it labeled Aquisição/Conversão/Retenção, connected by dashed spokes and solid cycle arrows between the 3 outer nodes.
2. Click the hub: the explorer below opens the Marca panel, showing its entregáveis with colored "Bäche faz" tags, then a second list headed "+ Conteúdo" with 3 more tagged items.
3. Click each of the 3 outer nodes: correct panel opens, tags render correctly (`Conversão` panel should show one item tagged "Sua equipe opera" in a visually distinct muted style; `Aquisição` panel should show one item tagged "Bäche dirige" in gold).
4. Resize the browser under 980px width: explorer becomes an accordion, ring becomes compact (no side labels), still 1 hub + 3 nodes, still clickable.
5. Keyboard: Tab to a node, Enter/Space activates it; arrow keys move focus between rail tabs on desktop.

If anything above fails, fix before committing — this is the riskiest task in the plan.

- [ ] **Step 9: Grep-verify old content is gone**

Run: `grep -c "Método Protagonista\|MÉTODO<br>PROTAGONISTA\|metodo-loops\|Fase 1\|Fase 2\|Fase 3\|Fase 4\|Fase 5\|Fase 6" index.html`
Expected: `0` (footer link at ~line 5046 still says "O Método Protagonista" — that's fine, Task 10 handles the footer separately; if this grep catches that footer line, subtract 1 from your mental count and confirm the rest are 0).

- [ ] **Step 10: Commit**

```bash
git add index.html
git commit -m "feat(metodo): mapa de 4 frentes + flywheel + entregaveis com etiqueta de responsabilidade"
```

---

### Task 4: `#plano` — remove old tier names, rename to Raio-X

**Files:**
- Modify: `index.html` (`#plano`, currently lines 4483-4545)

**Interfaces:**
- Consumes: nothing
- Produces: nothing later tasks depend on

- [ ] **Step 1: Rewrite step 1's title**

Old string:

```html
          <div class="plano-step-title">Você faz o Diagnóstico</div>
```

New string:

```html
          <div class="plano-step-title">Você faz o Raio-X</div>
```

- [ ] **Step 2: Rewrite step 2's description and sub-bullet**

Old string:

```html
          <div class="plano-step-title">A Bäche dirige</div>
          <p class="plano-step-desc">Você escolhe entre Sprint e Retainer, e a gente executa as 6 fases do Método: do posicionamento ao tráfego. Você só precisa aparecer, um dia de gravação por mês.</p>
          <ul class="plano-step-items">
            <li class="plano-step-item">As 6 fases do Método rodando por você</li>
            <li class="plano-step-item">Um dia de gravação vira 30 dias de presença</li>
          </ul>
```

New string:

```html
          <div class="plano-step-title">A Bäche dirige</div>
          <p class="plano-step-desc">Você escolhe o plano que cabe no seu momento, e a gente toca as 4 frentes de crescimento: marca, aquisição, conversão e retenção. Você só precisa aparecer, um dia de gravação por mês.</p>
          <ul class="plano-step-items">
            <li class="plano-step-item">As 4 frentes rodando por você</li>
            <li class="plano-step-item">Um dia de gravação vira 30 dias de presença</li>
          </ul>
```

- [ ] **Step 3: Update the closing CTA text**

Old string:

```html
        <div class="plano-result-cta">
          <a href="#contato" class="btn-primary" data-modal="diagnostico">
            Agendar Diagnóstico Gratuito
```

New string:

```html
        <div class="plano-result-cta">
          <a href="#contato" class="btn-primary" data-modal="diagnostico">
            Agendar meu Raio-X gratuito
```

- [ ] **Step 4: Verify**

Run: `grep -n "Sprint e Retainer\|6 fases do Método" index.html`
Expected: no output.

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "fix(plano): remove tiers antigos do passo 2, renomeia CTA para Raio-X"
```

---

### Task 5: `#diferenciais` — rename the "Direção Cênica" column

**Files:**
- Modify: `index.html` (`#diferenciais` table, currently lines 4550-4617)

**Interfaces:**
- Consumes: nothing
- Produces: nothing later tasks depend on

- [ ] **Step 1: Rename the column header**

Old string:

```html
              <th>Direção Cênica</th>
```

New string:

```html
              <th>Direção sênior, não mão de obra avulsa</th>
```

- [ ] **Step 2: Rename all 5 `data-label` attributes for that column** (`replace_all`)

Old string: `data-label="Direção Cênica"`
New string: `data-label="Direção sênior"`

Use `replace_all: true` — this string appears 5 times (once per competitor row) and every occurrence needs the same change.

- [ ] **Step 3: Verify**

Run: `grep -n "Direção Cênica" index.html`
Expected: 0 matches inside `#diferenciais` (matches may still remain elsewhere in the file — founders section and JSON-LD keep this phrase legitimately as a role title, not as a comparison-table column; Task 11's final QA distinguishes these).

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "fix(diferenciais): coluna vira direcao senior, tira nome de fase antiga"
```

---

### Task 6: `#transformacao` → Motor de 90 dias

**Files:**
- Modify: `index.html` (`#transformacao`, currently lines 4645-4692)

**Interfaces:**
- Consumes: nothing
- Produces: nothing later tasks depend on

- [ ] **Step 1: Replace the header**

Old string:

```html
      <div class="transformacao-header reveal">
        <div class="section-label">O que muda</div>
        <h2 class="section-title">Imagine sua clínica<br/>daqui a <em>90 dias.</em></h2>
        <p class="transformacao-sub">Especialistas que trabalham com a Bäche relatam essas transformações nos primeiros três meses.</p>
      </div>
```

New string:

```html
      <div class="transformacao-header reveal">
        <div class="section-label">Como trabalhamos</div>
        <h2 class="section-title">O motor de<br/><em>90 dias.</em></h2>
        <p class="transformacao-sub">A Bäche trata a sua clínica como você trata um paciente: diagnóstico completo, prescrição priorizada, tratamento por protocolos e retorno medido, em ciclos de 90 dias.</p>
      </div>
```

- [ ] **Step 2: Replace the 4 cards**

Old string:

```html
        <div class="transf-item stagger-child reveal">
          <div class="transf-item-num">01</div>
          <div class="transf-item-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/><path d="m9 16 2 2 4-4"/></svg></div>
          <div class="transf-item-title">Agenda particular com demanda consistente</div>
          <p class="transf-item-desc"><em>Sem depender de indicação ou convênio para pagar as contas.</em> Pacientes chegam pelo seu posicionamento — antes de ver o preço.</p>
        </div>

        <div class="transf-item stagger-child reveal reveal-delay-1">
          <div class="transf-item-num">02</div>
          <div class="transf-item-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="8" r="6"/><path d="M18.09 10.37A6 6 0 1 1 10.34 18"/><path d="M7 6h1v4"/><path d="m16.71 13.88.7.71-2.82 2.82"/></svg></div>
          <div class="transf-item-title">Cobrando premium — sem precisar justificar</div>
          <p class="transf-item-desc"><em>O paciente que chega já conhece seu trabalho.</em> A primeira pergunta não é mais sobre preço ou plano de saúde.</p>
        </div>

        <div class="transf-item stagger-child reveal reveal-delay-2">
          <div class="transf-item-num">03</div>
          <div class="transf-item-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 4.4-5.5 9.3-7.3 10.8a1 1 0 0 1-1.4 0C9.5 19.3 4 14.4 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/></svg></div>
          <div class="transf-item-title">Referência reconhecida da especialidade na região</div>
          <p class="transf-item-desc"><em>Colegas indicam, pacientes procuram, mídia consulta.</em> Sua autoridade chegou antes de você — exatamente onde deve estar.</p>
        </div>

        <div class="transf-item stagger-child reveal reveal-delay-3">
          <div class="transf-item-num">04</div>
          <div class="transf-item-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/></svg></div>
          <div class="transf-item-title">Equipe que converte — não que apenas informa</div>
          <p class="transf-item-desc"><em>Resposta ao paciente em menos de 5 minutos. Mais de 40% dos contatos viram consulta agendada.</em> A secretária virou parte da estratégia de crescimento.</p>
        </div>
```

New string:

```html
        <div class="transf-item stagger-child reveal">
          <div class="transf-item-num">01</div>
          <div class="transf-item-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/><path d="m9 16 2 2 4-4"/></svg></div>
          <div class="transf-item-title">01 Diagnóstico <span style="font-weight:400;opacity:.6;font-size:13px;">· Semanas 1-2</span></div>
          <p class="transf-item-desc"><em>Hoje você sabe se a agenda está cheia. Não sabe por quê, nem qual das quatro frentes está segurando o resultado.</em> Exame completo das 4 frentes, com os números da sua clínica na mesa.</p>
        </div>

        <div class="transf-item stagger-child reveal reveal-delay-1">
          <div class="transf-item-num">02</div>
          <div class="transf-item-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="8" r="6"/><path d="M18.09 10.37A6 6 0 1 1 10.34 18"/><path d="M7 6h1v4"/><path d="m16.71 13.88.7.71-2.82 2.82"/></svg></div>
          <div class="transf-item-title">02 Prescrição <span style="font-weight:400;opacity:.6;font-size:13px;">· Semana 3</span></div>
          <p class="transf-item-desc"><em>Plano de tratamento de 90 dias.</em> Poucas apostas, cada uma com meta e responsável. Nada de lista de tarefas genérica.</p>
        </div>

        <div class="transf-item stagger-child reveal reveal-delay-2">
          <div class="transf-item-num">03</div>
          <div class="transf-item-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 4.4-5.5 9.3-7.3 10.8a1 1 0 0 1-1.4 0C9.5 19.3 4 14.4 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/></svg></div>
          <div class="transf-item-title">03 Tratamento <span style="font-weight:400;opacity:.6;font-size:13px;">· Semanas 4-12</span></div>
          <p class="transf-item-desc"><em>Protocolos de cada frente rodando.</em> Leitura quinzenal dos números, você não espera 90 dias pra saber se está funcionando.</p>
        </div>

        <div class="transf-item stagger-child reveal reveal-delay-3">
          <div class="transf-item-num">04</div>
          <div class="transf-item-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/></svg></div>
          <div class="transf-item-title">04 Retorno <span style="font-weight:400;opacity:.6;font-size:13px;">· Semana 13</span></div>
          <p class="transf-item-desc"><em>Veredito de cada aposta: dobrar, manter ou cancelar.</em> O resultado na mesa desenha o próximo ciclo. A renovação nunca é por inércia.</p>
        </div>
```

- [ ] **Step 3: Add "A régua do motor" block and update the CTA, right after the grid**

Old string:

```html
      </div>

      <div class="transformacao-cta reveal">
        <a href="#contato" class="btn-primary" data-modal="diagnostico" style="font-size: 15px; padding: 20px 48px;">
          Agendar Diagnóstico Gratuito
```

New string:

```html
      </div>

      <div class="transformacao-regua reveal" style="max-width:640px;margin:44px auto 0;text-align:center;">
        <div class="section-label" style="justify-content:center;margin-bottom:10px;">A régua do motor</div>
        <p style="color:var(--text-secondary);line-height:1.6;">O painel único (custo por paciente, valor do paciente ao longo do tempo, ocupação, margem) é montado no Diagnóstico, lido nas quinzenais do Tratamento e fecha o veredito no Retorno. Cada frente do mapa tem seus indicadores, cada fase do ciclo os lê.</p>
        <p style="color:var(--nevoa);line-height:1.6;margin-top:12px;"><strong>O retorno abre o próximo ciclo.</strong> A renovação é decidida com o resultado na mesa, nunca por inércia.</p>
      </div>

      <div class="transformacao-cta reveal">
        <a href="#contato" class="btn-primary" data-modal="diagnostico" style="font-size: 15px; padding: 20px 48px;">
          Agendar meu Raio-X gratuito
```

- [ ] **Step 4: Verify**

Run: `grep -n "Imagine sua clínica\|Mais de 40% dos contatos" index.html`
Expected: no output.

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "feat(motor): transformacao vira motor de 90 dias com as 4 fases do brief"
```

---

### Task 7: `#produtos` → 3 planos sem preço + ancoragem

**Files:**
- Modify: `index.html` (`#produtos`, currently lines 4697-4794)

**Interfaces:**
- Consumes: nothing
- Produces: nothing later tasks depend on

- [ ] **Step 1: Replace the header**

Old string:

```html
        <div class="reveal">
          <div class="section-label">Esteira de Serviços</div>
          <h2 class="section-title">Escolha onde<br/>começar</h2>
        </div>
        <p class="produtos-desc reveal reveal-delay-2">
          Uma jornada desenhada para especialistas sérios — do primeiro diagnóstico até a autoridade total na sua especialidade, com cada etapa validada e acompanhada de perto.
        </p>
```

New string:

```html
        <div class="reveal">
          <div class="section-label">Planos</div>
          <h2 class="section-title">Escolha a<br/>abrangência</h2>
        </div>
        <p class="produtos-desc reveal reveal-delay-2">
          As 4 frentes de crescimento, do jeito que cabe na sua clínica hoje. Sem surpresa de escopo, sem letra miúda.
        </p>
```

- [ ] **Step 2: Replace all 4 product cards with 3 plan cards**

Old string (everything from the Diagnóstico card through the closing `</div>` of the Palco card, i.e. the entire `.produtos-grid` inner content):

```html
      <div class="produtos-grid">

        <!-- Diagnóstico -->
        <div class="product-card reveal">
          <div class="product-tag">Comece aqui</div>
          <div class="product-name">Diagnóstico Bäche</div>
          <div class="product-price-free-wrap">
            <div class="product-price-strike">R$1.500</div>
            <div class="product-price-free">Gratuito</div>
            <div class="product-price-free-note">por tempo limitado</div>
          </div>
          <div class="product-price-label" style="margin-top:12px;">sessão única · 2 horas · via call</div>
          <p class="product-desc">
            Em 2 horas, você entende exatamente o que está impedindo pacientes particulares de chegarem até você — e sai com um plano de ação concreto, independente de seguir conosco.
          </p>
          <ul class="product-features">
            <li class="product-feature">Auditoria completa de presença digital</li>
            <li class="product-feature">Diagnóstico de posicionamento</li>
            <li class="product-feature">Mapa de oportunidades</li>
            <li class="product-feature">Plano de ação 30 dias</li>
          </ul>
          <a href="#contato" class="product-cta dark" data-modal="diagnostico">Agendar diagnóstico gratuito</a>
        </div>

        <!-- Sprint -->
        <div class="product-card reveal reveal-delay-1">
          <div class="product-type-label">Projeto único · 30 dias</div>
          <div class="product-tag">Sprint de Fundação</div>
          <div class="product-name">Sprint Ignição</div>
          <div class="product-price-label" style="margin-bottom:24px; font-size:13px; color:rgba(13,12,20,0.50);">Entrega completa em um projeto fechado</div>
          <p class="product-desc">
            Construímos as bases da sua autoridade de marca em 30 dias: posicionamento, arquétipo, produção de conteúdo e o primeiro grande banco de autoridade da sua carreira.
          </p>
          <ul class="product-features">
            <li class="product-feature">Brand audit + arquétipo de marca</li>
            <li class="product-feature">2 sessões de preparação de presença</li>
            <li class="product-feature">1 dia completo de gravação dirigida</li>
            <li class="product-feature">Setup de funil + plano 90 dias</li>
          </ul>
          <a href="#contato" class="product-cta dark" data-modal="diagnostico">Quero meu Sprint</a>
        </div>

        <!-- Retainer — FEATURED -->
        <div class="product-card featured reveal reveal-delay-2">
          <div class="product-badge">Recomendado para começar</div>
          <div class="product-type-label">Retainer mensal</div>
          <div class="product-tag">Gestão Contínua</div>
          <div class="product-name">Retainer Presença</div>
          <div class="product-price-label" style="margin-bottom:24px; color:rgba(255,255,255,0.5); font-size:13px;">Investimento mensal · com garantia de resultado</div>
          <p class="product-desc">
            Gestão completa da sua presença e performance mês a mês. Você foca na clínica — nós cuidamos da autoridade, dos pacientes e dos números.
          </p>
          <ul class="product-features">
            <li class="product-feature">1 dia/mês de gravação dirigida</li>
            <li class="product-feature">Tráfego pago + retorno sobre a mídia acompanhado</li>
            <li class="product-feature">Dashboard de resultados em tempo real</li>
            <li class="product-feature">Treinamento da equipe comercial</li>
            <li class="product-feature">Consultoria estratégica quinzenal</li>
            <li class="product-feature">Garantia de resultado 90 dias</li>
          </ul>
          <a href="#contato" class="product-cta light" data-modal="diagnostico">Quero o Retainer</a>
        </div>

        <!-- Palco -->
        <div class="product-card reveal reveal-delay-3">
          <div class="product-type-label">Setup + Mensal</div>
          <div class="product-tag">Dominância de Mercado</div>
          <div class="product-name">Programa Palco</div>
          <div class="product-price-label" style="margin-bottom:24px; font-size:13px; color:rgba(13,12,20,0.50);">Sob consulta · vagas limitadas</div>
          <p class="product-desc">
            Para especialistas que querem dominar sua especialidade na cidade. Rebrand completo, estratégia multi-canal e posicionamento de autoridade máxima no mercado.
          </p>
          <ul class="product-features">
            <li class="product-feature">Tudo do Retainer Presença</li>
            <li class="product-feature">Rebrand completo da clínica</li>
            <li class="product-feature">Estratégia multi-canal</li>
            <li class="product-feature">Vídeo institucional profissional</li>
            <li class="product-feature">Preparação para mídia e keynotes</li>
            <li class="product-feature">Evento de lançamento de marca</li>
          </ul>
          <a href="#contato" class="product-cta dark" data-modal="diagnostico">Quero o Palco</a>
        </div>

      </div>
```

New string:

```html
      <div class="produtos-grid">

        <!-- Essencial -->
        <div class="product-card reveal">
          <div class="product-type-label">Porta de entrada</div>
          <div class="product-tag">Comece a estruturar</div>
          <div class="product-name">Essencial</div>
          <div class="product-price-label" style="margin-bottom:24px; font-size:13px; color:rgba(13,12,20,0.50);">Para clínicas começando a estruturar marketing</div>
          <p class="product-desc">
            2 a 3 frentes priorizadas no seu Raio-X, painel único e reuniões quinzenais. Foco no vazamento de receita mais óbvio primeiro.
          </p>
          <ul class="product-features">
            <li class="product-feature">2 a 3 frentes priorizadas no Raio-X</li>
            <li class="product-feature">Painel único e reuniões quinzenais</li>
            <li class="product-feature">Foco no vazamento de receita mais óbvio</li>
            <li class="product-feature" style="opacity:.5;text-decoration:line-through;">Conteúdo e vídeo</li>
          </ul>
          <a href="#contato" class="product-cta dark" data-modal="diagnostico">Agendar meu Raio-X gratuito</a>
        </div>

        <!-- Ciclo completo — FEATURED -->
        <div class="product-card featured reveal reveal-delay-1">
          <div class="product-badge">O mais escolhido</div>
          <div class="product-type-label">Retainer mensal</div>
          <div class="product-tag">O caso típico da carteira</div>
          <div class="product-name">Ciclo completo</div>
          <div class="product-price-label" style="margin-bottom:24px; color:rgba(255,255,255,0.5); font-size:13px;">As 4 frentes rodando junto com você</div>
          <p class="product-desc">
            As 4 frentes de crescimento, painel único e quinzenais, 1 dia de gravação em lote por mês, com gravação, edição e postagem por conta da Bäche.
          </p>
          <ul class="product-features">
            <li class="product-feature">As 4 frentes: marca, aquisição, conversão e retenção</li>
            <li class="product-feature">Painel único e reuniões quinzenais</li>
            <li class="product-feature">1 dia de gravação em lote por mês</li>
            <li class="product-feature">Gravação, edição e postagem pela Bäche</li>
            <li class="product-feature">Direção editorial e treino de câmera</li>
          </ul>
          <a href="#contato" class="product-cta light" data-modal="diagnostico">Agendar meu Raio-X gratuito</a>
        </div>

        <!-- Rede -->
        <div class="product-card reveal reveal-delay-2">
          <div class="product-type-label">Multiunidade</div>
          <div class="product-tag">Rede ou vários médicos</div>
          <div class="product-name">Rede</div>
          <div class="product-price-label" style="margin-bottom:24px; font-size:13px; color:rgba(13,12,20,0.50);">As 4 frentes replicadas por unidade</div>
          <p class="product-desc">
            Para rede com mais de uma unidade ou vários médicos. As 4 frentes replicadas, relatório consolidado e governança de marca entre unidades.
          </p>
          <ul class="product-features">
            <li class="product-feature">As 4 frentes replicadas por unidade</li>
            <li class="product-feature">Relatório consolidado entre unidades</li>
            <li class="product-feature">Conteúdo centralizado ou por unidade</li>
            <li class="product-feature">Governança de marca</li>
          </ul>
          <a href="#contato" class="product-cta dark" data-modal="diagnostico">Agendar meu Raio-X gratuito</a>
        </div>

      </div>

      <blockquote class="dor-quote reveal" style="margin:56px auto 0;max-width:720px;">
        Um head de marketing sênior interno custa entre R$15 e 25 mil por mês de salário, mais encargos e o risco de contratar errado. A Bäche entrega esse nível de direção por uma fração, sem vínculo, com método pronto. E parte do que ganhamos está atrelada ao seu resultado.
      </blockquote>
```

- [ ] **Step 3: Verify**

Run: `grep -c "Diagnóstico Bäche\|Sprint Ignição\|Retainer Presença\|Programa Palco\|R\$1.500" index.html`
Expected: count should now only reflect remaining mentions in the footer (Task 10) and JSON-LD (already fixed in Task 1) — 0 within `#produtos` specifically. Spot-check with `grep -n "Sprint Ignição\|Retainer Presença\|Programa Palco" index.html` and confirm none of the remaining lines are between the `<section id="produtos">` and its closing `</section>`.

- [ ] **Step 4: Visual check**

Open `http://localhost:3000#produtos` (dev server from Task 3 may still be running). Confirm: 3 cards render, "Ciclo completo" (middle) has the gold "O mais escolhido" ribbon and solid purple background, "Essencial" shows the "Conteúdo e vídeo" line struck through, ancoragem paragraph renders as a centered blockquote below the grid.

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "feat(oferta): 4 tiers com preco viram 3 planos por abrangencia + ancoragem"
```

---

### Task 8: `#garantia` — risco compartilhado

**Files:**
- Modify: `index.html` (`#garantia`, currently lines 4799-4826)

**Interfaces:**
- Consumes: nothing
- Produces: nothing later tasks depend on

- [ ] **Step 1: Replace the title and body text**

Old string:

```html
          <h2 class="garantia-title">Resultado<br/>mensurável ou<br/>trabalhamos de graça.</h2>
        </div>
        <p class="garantia-text reveal reveal-delay-1">
          Se em 90 dias a meta de novos pacientes particulares acordada em contrato não for atingida, <strong>você escolhe</strong>: a Bäche trabalha o mês seguinte sem custo, ou devolve integralmente o último fee.
        </p>
```

New string:

```html
          <h2 class="garantia-title">Resultado<br/>medido, com<br/>a gente no jogo.</h2>
        </div>
        <p class="garantia-text reveal reveal-delay-1">
          Parte do que ganhamos está atrelada ao seu crescimento. <strong>Não é uma promessa de devolução</strong>; é ter a pele em jogo no mesmo número que você quer ver subir.
        </p>
```

- [ ] **Step 2: Verify**

Run: `grep -n "trabalhamos de graça\|devolve integralmente o último fee" index.html`
Expected: no output.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "fix(garantia): suaviza para risco compartilhado, remove devolucao de fee"
```

---

### Task 9: `#faq` — item 1 sem nome de tier antigo

**Files:**
- Modify: `index.html` (`#faq` item 1, currently lines 4894-4904)

**Interfaces:**
- Consumes: nothing
- Produces: nothing later tasks depend on

- [ ] **Step 1: Replace the answer**

Old string:

```html
            <div class="faq-answer-inner">
              Sua agência atual provavelmente cobra R$2.000/mês e não gera paciente particular. O Sprint Ignição se paga com 2 novos pacientes — e temos <strong>garantia de resultado em 90 dias</strong>. Nenhum concorrente oferece isso. A pergunta certa não é "quanto custa?" — é "quanto custa continuar igual?".
            </div>
```

New string:

```html
            <div class="faq-answer-inner">
              Sua agência atual provavelmente cobra R$2.000 por mês e não gera paciente particular. Com a Bäche, parte do que cobramos está atrelada ao seu resultado, o risco começa com a gente. A pergunta certa não é "quanto custa?", é "quanto custa continuar igual?".
            </div>
```

- [ ] **Step 2: Verify**

Run: `grep -n "Sprint Ignição se paga" index.html`
Expected: no output.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "fix(faq): remove nome de tier antigo, reforca risco compartilhado"
```

---

### Task 10: CTA sweep + footer + FQ_GAR + modal submit label

Handles every remaining CTA/footer/modal instance NOT already touched by Tasks 3, 4, 6, 7, 9. Run this task after those, since it assumes their inline CTA text is already updated.

**Files:**
- Modify: `index.html`:
  - Nav CTA, currently lines 4168-4170
  - Mobile menu CTA, currently lines 4185-4190
  - Hero primary CTA, currently lines 4221-4226
  - Final CTA section (`#contato`), currently lines 4984-4994
  - Footer links, currently lines 5037-5055
  - `FQ_GAR` array, currently lines 6090-6097
  - Modal submit label override, currently line 6144

**Interfaces:**
- Consumes: assumes Tasks 3, 4, 6, 7, 9 already changed their own inline CTA text — don't re-touch `#metodo`, `#plano`, `#transformacao`, `#produtos`, `#faq` in this task
- Produces: nothing later tasks depend on

- [ ] **Step 1: Nav CTA**

Old string:

```html
    <a href="#contato" class="nav-cta" data-modal="diagnostico" aria-label="Agendar Diagnóstico Gratuito">
      Diagnóstico Gratuito
    </a>
```

New string:

```html
    <a href="#contato" class="nav-cta" data-modal="diagnostico" aria-label="Agendar meu Raio-X gratuito">
      Raio-X gratuito
    </a>
```

- [ ] **Step 2: Mobile menu CTA**

Old string:

```html
      <a href="#contato" class="btn-gold mobile-menu-cta" data-modal="diagnostico">
        Diagnóstico Gratuito
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
```

New string:

```html
      <a href="#contato" class="btn-gold mobile-menu-cta" data-modal="diagnostico">
        Raio-X gratuito
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
```

- [ ] **Step 3: Hero primary CTA**

Old string:

```html
        <a href="#contato" class="btn-primary" data-modal="diagnostico">
          Agendar Diagnóstico Gratuito
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </a>
        <a href="#plano" class="btn-ghost">
```

New string:

```html
        <a href="#contato" class="btn-primary" data-modal="diagnostico">
          Agendar meu Raio-X gratuito
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </a>
        <a href="#plano" class="btn-ghost">
```

(This old_string is unique because it's the only `.btn-primary` immediately followed by a `.btn-ghost` linking to `#plano` — the hero pair. Confirm uniqueness with a grep before applying if unsure: `grep -n "Agendar Diagnóstico Gratuito" index.html` should show this as the only remaining hit after Tasks 3/4/6/7/9 land.)

- [ ] **Step 4: Final CTA section (`#contato`)**

Old string:

```html
      <p class="contato-sub reveal reveal-delay-2">
        Começamos com um Diagnóstico de 2 horas — sem custo, sem compromisso. Você entende exatamente o que está bloqueando sua agenda particular e sai com um plano de ação concreto. Se fizer sentido prosseguir, construímos juntos. Se não, o plano é seu.
      </p>
      <div class="contato-actions reveal reveal-delay-3">
        <a href="#contato" class="btn-gold glow-pulse" data-modal="diagnostico"
           aria-label="Agendar Diagnóstico Gratuito">
          Agendar Diagnóstico Gratuito
```

New string:

```html
      <p class="contato-sub reveal reveal-delay-2">
        Começamos com um Raio-X de 2 horas, sem custo, sem compromisso. Você entende exatamente o que está bloqueando sua agenda particular e sai com um plano de ação concreto. Se fizer sentido prosseguir, construímos juntos. Se não, o plano é seu.
      </p>
      <div class="contato-actions reveal reveal-delay-3">
        <a href="#contato" class="btn-gold glow-pulse" data-modal="diagnostico"
           aria-label="Agendar meu Raio-X gratuito">
          Agendar meu Raio-X gratuito
```

- [ ] **Step 5: Footer — Serviços column**

Old string:

```html
          <div class="footer-links-title">Serviços</div>
          <ul class="footer-links-list">
            <li><a href="#produtos">Diagnóstico Gratuito</a></li>
            <li><a href="#produtos">Sprint Ignição</a></li>
            <li><a href="#produtos">Retainer Presença</a></li>
            <li><a href="#produtos">Programa Palco</a></li>
          </ul>
```

New string:

```html
          <div class="footer-links-title">Serviços</div>
          <ul class="footer-links-list">
            <li><a href="#contato">Raio-X gratuito</a></li>
            <li><a href="#produtos">Essencial</a></li>
            <li><a href="#produtos">Ciclo completo</a></li>
            <li><a href="#produtos">Rede</a></li>
          </ul>
```

- [ ] **Step 6: Footer — Empresa column**

Old string:

```html
            <li><a href="#metodo">O Método Protagonista</a></li>
```

New string:

```html
            <li><a href="#metodo">Nosso método</a></li>
```

- [ ] **Step 7: Footer — Contato column**

Old string:

```html
            <li><a href="#contato">Agendar Diagnóstico</a></li>
```

New string:

```html
            <li><a href="#contato">Agendar Raio-X</a></li>
```

- [ ] **Step 8: `FQ_GAR` remap**

Old string:

```javascript
    const FQ_GAR = [
      ['Apareço igual a todo mundo', 'Marca & Mensagem'],
      ['Travo na câmera / não apareço', 'Direção Cênica'],
      ['Anúncio traz paciente errado ou nenhum', 'Aquisição'],
      ['Lead chega no WhatsApp e não fecha', 'Conversão'],
      ['Não sei meus números (CAC, LTV...)', 'Mensuração'],
      ['Paciente não volta nem indica', 'Fidelização']
    ];
```

New string:

```javascript
    const FQ_GAR = [
      ['Apareço igual a todo mundo', 'Marca'],
      ['Travo na câmera / não apareço', 'Conteúdo'],
      ['Anúncio traz paciente errado ou nenhum', 'Aquisição'],
      ['Lead chega no WhatsApp e não fecha', 'Conversão'],
      ['Não sei meu custo por paciente nem quanto ele vale', 'Régua do motor'],
      ['Paciente não volta nem indica', 'Retenção']
    ];
```

- [ ] **Step 9: Modal submit label, final step**

Old string:

```javascript
      submitLabel.textContent = fqStep === 3 ? 'Quero meu Diagnóstico Gratuito' : 'Continuar';
```

New string:

```javascript
      submitLabel.textContent = fqStep === 3 ? 'Quero meu Raio-X gratuito' : 'Continuar';
```

- [ ] **Step 10: Verify**

Run: `grep -n "Diagnóstico Gratuito\|Sprint Ignição\|Retainer Presença\|Programa Palco\|Método Protagonista\|Mensuração'\|Fidelização'\|Marca & Mensagem'" index.html`
Expected: no output at all.

Run: `grep -c "Raio-X" index.html`
Expected: a healthy double-digit count (every CTA + footer + modal + JSON-LD instance).

- [ ] **Step 11: Commit**

```bash
git add index.html
git commit -m "fix(cta): unifica todo CTA em Raio-X gratuito, remapeia FQ_GAR pras 4 frentes"
```

---

### Task 11: Final acceptance QA

Runs the spec's full acceptance checklist against the finished file. No content changes expected in this task — only fixes if something below fails.

**Files:**
- Modify: `index.html` (only if a check below fails)

**Interfaces:**
- Consumes: the completed state of all 10 previous tasks
- Produces: nothing (terminal task)

- [ ] **Step 1: Old-model expression sweep**

Run: `grep -n "Método Protagonista\|Sprint Ignição\|Retainer Presença\|Programa Palco" index.html`
Expected: **zero matches** anywhere in the file, including JSON-LD.

Run: `grep -n "Direção Cênica" index.html`
Expected: matches **only** in the `#fundadores` section (founder role/skill, unchanged per spec) and the JSON-LD `founder`/`knowsAbout` entries (unchanged per spec). If a match shows up inside `#diferenciais`, `#metodo`, or `FQ_GAR`, Task 5, 3, or 10 respectively has a bug — fix it now.

- [ ] **Step 2: No plan/tier price anywhere**

Run: `grep -n "R\$" index.html`
Expected matches, and **only** these: the FAQ's `R$2.000 por mês` (competitor's hypothetical price, Task 9), and the qualification modal's revenue brackets (`Até R$30k`, `R$30-80k`, `R$80-200k`, `R$200k+`, `Até R$100k`, `R$100-300k`, `R$300k-1M`, `R$1M+` — client's own revenue, untouched, out of scope) — plus the new ancoragem paragraph's `R$15 e 25 mil` (that one describes a hypothetical internal hire's salary, not a Bäche plan price, and is explicitly required by the spec). Any other match is a bug.

- [ ] **Step 3: Structural checks on the new frentes explorer**

Run: `node -e "const s=require('fs').readFileSync('index.html','utf8'); const m=s.match(/const FRENTES = (\[[\s\S]*?\n      \]);/); if(!m) throw new Error('FRENTES array not found'); const arr=eval(m[1]); if(arr.length!==4) throw new Error('expected 4 frentes, got '+arr.length); const names=arr.map(f=>f.n).join(','); if(names!=='Marca,Aquisição,Conversão,Retenção') throw new Error('unexpected frente order: '+names); if(!arr[0].conteudo || arr[0].conteudo.length<1) throw new Error('Marca missing conteudo sub-block'); console.log('OK', names);"`
Expected: `OK Marca,Aquisição,Conversão,Retenção`

- [ ] **Step 4: Visual QA pass (single session, one final screenshot)**

Start `npx serve -p 3000 .` if not already running. Open the page and, in one evaluate call, check: `#metodo` renders 4 clickable ring nodes, `#produtos` renders exactly 3 `.product-card` elements with one `.featured`, `#garantia` badge still shows "90", `#faq` accordion still opens/closes. Take one full-page screenshot at desktop width and one at a mobile width (390px) as the final visual record — no more than these two.

- [ ] **Step 5: Run the spec's checklist literally**

Open `docs/superpowers/specs/2026-07-06-metodo-oferta-design.md` and check off every item in "Checklist de aceite" against the current file state. Any unchecked item means a task above needs a follow-up fix before this plan is done.

- [ ] **Step 6: Commit (only if Steps 1-3 required fixes)**

```bash
git add index.html
git commit -m "fix(qa): ajustes finais da varredura de aceite pos reestruturacao"
```

If no fixes were needed, skip this commit — there's nothing to commit.
