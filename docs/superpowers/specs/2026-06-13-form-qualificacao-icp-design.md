# Formulário de qualificação ICP por etapas — Bäche

Data: 2026-06-13 · Status: design aprovado (protótipo validado, fork médico×clínica)

## Objetivo
Trocar o modal de Diagnóstico (3 campos, 1 etapa) por um **formulário multi-step que qualifica o lead por ICP-fit**, ramificando entre **médico** e **clínica** (negócios e prestação diferentes). Frame: "mini-diagnóstico de 60s". Não bloqueia ninguém (soft-score).

## Decisões
- **Soft-score**: captura todos, nunca bloqueia. Calcula fit interno (quente/morno/frio) e grava no ClickUp como prioridade. Invisível pro lead.
- **Público**: saúde em geral (médicos, dentistas, outros profissionais de alto ticket).
- **Fork médico × clínica** na etapa 1: muda perguntas, faixas e score.
- **Contato na última etapa** (compromisso/consistência). [default; revisável]
- **4 etapas**: Fork+cidade → Perfil (trilha) → Situação/gargalo (trilha) → Contato.
- **Cards de escolha única** (toque rápido, mobile-first), não selects.

## Estrutura das etapas

**Etapa 1 — comum:** "Você é médico ou clínica?" (fork, 2 cards) + Cidade/UF.

**Etapa 2 — Perfil (ramifica):**
- *Médico:* especialidade (texto) · atende [Particular / Misto / Convênio quero migrar / Só convênio] · onde atua [Consultório próprio / Clínica de terceiros / Hospital / Mais de um].
- *Clínica:* nº de médicos [1–3 / 4–10 / 10+ / Só eu, quero crescer] · especialidades (texto) · **papel** [Dono-sócio / Gestor-marketing / Médico da clínica].

**Etapa 3 — Situação + gargalo (ramifica):**
- *Médico:* faturamento particular/mês [Até 30k / 30–80k / 80–200k / 200k+] · "você aparece/produz conteúdo?" [Nunca / Travo na câmera / Regular] · maior gargalo (6 opções → 6 fases).
- *Clínica:* faturamento da clínica/mês [Até 100k / 100–300k / 300k–1M / 1M+] · equipe de marketing [Interna / Agência / Secretária / Ninguém] · maior gargalo (6 opções).

**Etapa 4 — comum:** Nome · WhatsApp · E-mail → submit "Quero meu Diagnóstico Gratuito".

Gargalo (ambas trilhas), mapeado às fases: Apareço igual a todos (Marca) · Travo na câmera (Direção Cênica) · Anúncio errado/nenhum (Aquisição) · Lead não fecha (Conversão) · Não sei meus números (Mensuração) · Não volta nem indica (Fidelização).

## Soft-score
Soma de pesos das respostas; faixas: **≥8 quente · 5–7 morno · <5 frio**.
- Pesos comuns: faturamento 0–3; gargalo +1.
- Médico: atende (Particular 3 / Misto·migrar 2 / Só convênio 0); onde (próprio 2 / outros 1); conteúdo (Travo 3 / Nunca 2 / Regular 1).
- Clínica: nº médicos (1); papel (Dono 3 / Gestor 2 / Médico 0); marketing (com budget 2 / secretária·ninguém 1).
- (Pesos finais calibráveis; valores acima são ponto de partida do protótipo.)

## Integração (dados)
- **ClickUp** (lista existente "Sessão Estratégica", token/list atuais): criar task com `name = "Sessão Estratégica — {nome} ({Médico|Clínica})"`, **description** com TODAS as respostas formatadas + linha "Fit: {quente|morno|frio} (score N)", e **priority** pelo score (1 urgent=quente, 2 high=morno, 3 normal=frio). Custom fields WhatsApp/Email como hoje.
- **Sem criar custom fields novos no ClickUp agora** (description + priority resolvem). Evolução futura: campos dropdown por qualificador.
- **EmailJS**: confirmação ao lead, igual hoje.
- **Analytics**: `bacheTrack('generate_lead', { method, path, fit })`.

## UX / Acessibilidade
- Barra de progresso "Etapa X de 4" + voltar/continuar.
- "Continuar" exige a(s) resposta(s) obrigatória(s) da etapa (fork obrigatório na 1; contato validado na 4 com regex atual).
- Cards: `role`/teclado (Enter/Espaço), seleção única por grupo, foco visível.
- `prefers-reduced-motion`: sem animação de transição.
- Mobile: cards em 1–2 colunas, alvos ≥44px. Estilo/fontes/paleta do site (ouro/violeta/noite, Internacional/Satoshi).
- Estado de sucesso reaproveitado, com mensagem que varia por trilha.

## Fora de escopo
- Não há roteamento de conteúdo alternativo por fit (só score). Não há persistência de respostas parciais. Não cria campos novos no ClickUp. Não altera as outras seções da LP.

## Pendências/defaults a confirmar na revisão
- Contato no fim (vs início). · Conjunto de campos por trilha (manter vs cortar). · Pesos do score.
