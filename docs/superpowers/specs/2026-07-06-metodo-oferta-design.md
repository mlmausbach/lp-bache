# Reestruturação de método e oferta — Bäche

Data: 2026-07-06 · Status: em revisão (design aprovado em chat, aguardando revisão do arquivo)

Fonte: `brief-atualizacao-bache-site.md`. Este spec traduz o brief em decisões de arquitetura, mapeamento seção-a-seção e padrão de copy. Identidade visual (paleta, fontes, grid, componentes) permanece intocada — este é um trabalho de conteúdo, não de redesign.

## Objetivo

Substituir duas coisas no site: (1) o Método Protagonista (6 fases) por um mapa de 4 frentes + flywheel + motor de 90 dias + entregáveis com responsabilidade explícita; (2) os 4 tiers com preço por 3 planos sem preço, com âncora de valor. Regra-mãe: **substituir, não empilhar**. Nenhuma expressão do modelo antigo pode sobreviver em nenhuma página ou componente (ver checklist de aceite, item final).

## Padrão de copy: pains, gains e JTBD do ICP

Ajuste do Murillo sobre o design original: tradução de jargão (item "Vocabulário" abaixo) é necessária mas não suficiente — a copy precisa doer na dor real e mirar o ganho real do ICP. Toda copy nova escrita na implementação deve ser checada contra esta tabela, não só contra o glossário.

ICP tem dois subperfis com nuances diferentes — médico individual e clínica/dono — mapeados pelo próprio fork do formulário de qualificação já existente no site.

**Médico individual**

| Dor | Ganho buscado |
|---|---|
| Comparado por preço apesar de ser tecnicamente melhor ("aceita convênio?" antes de saber quem ele é) | Ser procurado antes de comparar preço, virar referência |
| Trava/constrangimento na câmera, some ou evita aparecer | Gravar 1 dia, ter presença o mês inteiro, sem virar refém da câmera |
| Já queimou dinheiro com agência/freela que não entendeu saúde ou CFM | Direção sênior de verdade, não mão de obra avulsa |
| Não sabe de onde vêm os pacientes nem quanto custou cada um — decide no escuro | Painel simples, controle, sem ansiedade |
| Depende de convênio/indicação, agenda imprevisível | Agenda particular previsível |
| Paciente que veio por preço some depois de uma consulta | Base que volta e indica, custo de aquisição caindo |

JTBD: *"preciso de mais paciente particular previsível, sem eu mesmo virar gestor de marketing"* (funcional) · *"preciso parar de me sentir exposto na câmera e de decidir no escuro"* (emocional) · *"preciso ser referência, não mais um nome genérico"* (social)

**Clínica / dono de múltiplas unidades** (pains do médico valem em escala, mais:)

| Dor | Ganho buscado |
|---|---|
| Resultado depende de qual médico está na cadeira | Marca maior que qualquer indivíduo, sistema sobrevive à saída de um médico |
| Sem consolidado entre unidades/médicos | Relatório consolidado, decisão com dado por unidade |
| Precisa justificar investimento de marketing pro sócio/financeiro | Número que encerra a discussão, não achismo |

JTBD: *"preciso de um sistema de crescimento que funcione em escala, não dependente de uma pessoa"* (funcional) · *"preciso parar de brigar internamente sobre se marketing funciona"* (emocional)

**Onde cada dor precisa aparecer na copy nova** (checklist de implementação):
- Frente Marca abre com a dor de ser comparado por preço / soar igual a todo mundo
- Frente Aquisição abre com a dependência de convênio/indicação
- Frente Conversão abre com o lead que morre no WhatsApp
- Frente Retenção abre com o paciente que some depois de uma consulta
- Motor · fase Diagnóstico abre com "decide no escuro"
- Entregáveis/etiqueta de responsabilidade ataca a desconfiança em quem executa (direção sênior vs mão de obra)
- Ancoragem de valor ataca a necessidade de justificar investimento
- Vilão de abertura ("Pare de decidir seu marketing no escuro") ataca a mesma dor de raiz do Diagnóstico

**Exemplos de calibragem de voz** (não são copy final, só travam o tom antes de escrever tudo):
- Marca (abertura do painel da frente): *"'Aceita convênio?' costuma ser a primeira pergunta, antes do paciente saber o que te torna diferente de qualquer outro especialista da cidade. Marca é o que muda a ordem dessa pergunta."*
- Motor · 01 Diagnóstico (abertura): *"Hoje você sabe se a agenda está cheia. Não sabe por quê, nem qual das quatro frentes está segurando o resultado. O Diagnóstico troca achismo por número: exame completo das 4 frentes, com os dados da sua clínica na mesa."*
- Vilão (abertura da seção `dor`): *"Pare de decidir seu marketing no escuro."*

Regra existente que continua valendo: sem travessão (—) na copy, variar construção de frase (ver memória `feedback-copy-sem-travessao`).

## Decisões de arquitetura

**A — Mapa + flywheel + entregáveis: um único explorer, não três peças separadas.**
Reaproveita o motor de ring/hub SVG que já existe (`metodoFw`, hoje 6 nós) reduzido a 4: **Marca no hub central**, **Aquisição/Conversão/Retenção orbitando**. Um único diagrama comunica as duas ideias do brief (hierarquia — Marca é o eixo do qual tudo depende — e flywheel — as três giram em ciclo). Todos os 4 nós são clicáveis (mudança necessária: hoje o hub é decorativo; passa a ser mais uma aba) e abrem o painel de detalhe abaixo (rail no desktop, acordeão no mobile — reaproveita o padrão ARIA tabs já implementado e validado). Cada painel mostra papel + frase-cliente + entregáveis com etiqueta de responsabilidade.

Motivo da escolha: reaproveita 100% do código de interação já existente e aprovado (`docs/superpowers/specs/2026-06-13-metodo-interativo-design.md`), menos superfície nova pra testar, e espelha a progressão do próprio brief (o quê → por que é ciclo → o que exatamente eu recebo) em vez de três seções repetindo a mesma informação.

**B — Motor de 90 dias substitui o conteúdo de `#transformacao`, não é seção nova.**
`#transformacao` hoje é um grid de 4 cards de resultado genérico ("imagine sua clínica daqui a 90 dias"), sem fases nem semanas — não é, como se poderia supor, uma versão disfarçada do motor. Ter as duas seções ("resultado em 90 dias" genérico e "motor de 90 dias" operacional) uma do lado da outra seria redundante. Reaproveita o grid de 4 cards (`.transf-item`) já existente, adicionando campo "quando" (Semanas 1-2, Semana 3, Semanas 4-12, Semana 13).

## Mapeamento seção a seção

Todos os ids de seção são mantidos (evita quebrar âncoras/analytics); muda o conteúdo interno e, onde indicado, o rótulo visível.

### `#hero` — sem mudança estrutural
Só o texto do CTA principal muda (ver CTA único, abaixo).

### `#stats` — mesma estrutura, 3 números corrigidos
`291.362` → faixa honesta ("centenas de milhares"); `41%` → idem; `25%` → idem (terceiro número com o mesmo problema de falsa precisão, brief citou só os 2 primeiros como exemplo mas a correção vale pros 3). Manter o disclaimer "Estimativas internas Bäche" abaixo.

### `#dor` — mesma estrutura, + linha de abertura nova
Adiciona o vilão *"Pare de decidir seu marketing no escuro"* como linha de abertura, antes da quote que já existe (`.dor-quote` permanece, não é substituída).

### `#guia` — sem mudança
A dualidade Performance+Branding continua válida e não conflita com o mapa de frentes (guia = por quê filosófico, mapa = o quê concreto).

### `#metodo` — vira "Mapa de 4 frentes + flywheel + entregáveis" (Decisão A)
- Label/título/tese reescritos: sai "6 fases em ordem causal", entra a lógica de 4 frentes + eixo de marca.
- Diagrama: ring/hub adaptado (Marca no centro, 3 frentes orbitando, setas de ciclo — reaproveita `metodoFw`). Texto de apoio do flywheel (parágrafo do brief sobre atrito alto no primeiro ciclo) abaixo do diagrama.
- Explorer (rail desktop / acordeão mobile, reaproveita `.metodo-explorer` / `.mx-tab` / `.mx-panel`): 4 painéis com papel + frase-cliente + lista de entregáveis. Cada entregável ganha etiqueta de responsabilidade (ver Componentes).
- Conteúdo (confirmado que a operação já existe e está testada) entra como subseção dentro do painel de **Marca** — não é uma 5ª frente.
- "Incluído em todo plano" (painel único + reunião quinzenal) vira uma faixa sempre visível abaixo do explorer, independente da aba selecionada — é infraestrutura do motor, nunca uma frente (regra-mãe é explícita nisso).
- Loops (`.metodo-loops`) removidos: a lógica de loop de aprendizado/econômico do método antigo não tem equivalente 1:1 no novo modelo, e a mensagem de recorrência já fica coberta pelo flywheel + pela nota de recorrência do motor. Manter este bloco duplicaria a mensagem de "é ciclo, não linha".
- Bridge/CTA final da seção: mantém os dois botões (primário → Raio-X, ghost → "Conhecer os planos" → `#produtos`), copy atualizada.

### `#plano` ("Como começar") — mesma estrutura, copy atualizada
Os 3 passos (Você faz o Diagnóstico / Bäche dirige / Você acompanha) continuam válidos como jornada comercial macro — só ajusta nomenclatura (Diagnóstico gratuito → Raio-X gratuito) e garante que não cita Sprint/Retainer por nome (hoje o passo 2 já é genérico o suficiente: "você escolhe entre Sprint e Retainer" precisa virar "você escolhe o plano que cabe no seu momento").

### `#diferenciais` — mesma tabela, 1 coluna renomeada
Coluna "Direção Cênica" (✕ pra todo concorrente, ✓ só pra Bäche) vira uma coluna sobre a etiqueta de responsabilidade: nenhum concorrente informa quem de fato executa cada entrega, a Bäche sim. Reaproveita a mesma estrutura ✓/✕/~ (`.check.yes`/`.check.no`). `attr-card` 1 (Produção de Autoridade Exclusiva) não cita literalmente "Direção Cênica" como fase, revisão é só polimento leve.

### `#transformacao` — vira "Motor de 90 dias" (Decisão B)
- Pull-quote de abertura: frase-síntese do brief (analogia médica: diagnóstico, prescrição, tratamento, retorno).
- 4 cards (reaproveita `.transf-item`) com campo novo "quando": 01 Diagnóstico (Semanas 1-2) → 02 Prescrição (Semana 3) → 03 Tratamento (Semanas 4-12) → 04 Retorno (Semana 13).
- "A régua do motor": mesmo conteúdo/copy do bloco "incluído em todo plano" do `#metodo` (não duplicar como texto diferente — é a mesma ideia, painel único lido em cada fase).
- Fecha com a nota de recorrência do brief.

### `#produtos` — vira "Planos" (3 cards, sem preço) + ancoragem
- Card do Diagnóstico/Raio-X sai da grade (deixa de ser um "tier" — vira CTA universal, ver item CTA). Sobram 3: **Essencial**, **Ciclo completo** (destacado), **Rede**.
- Ciclo completo reaproveita `.product-card.featured` + `.product-badge` (texto novo, ex.: "O mais escolhido").
- Essencial mostra explicitamente a exclusão de conteúdo/vídeo (linha esmaecida ou riscada, não só omissão silenciosa).
- Como a operação de conteúdo já existe e está testada (confirmado): Ciclo completo e Rede incluem gravação, edição e postagem por conta da Bäche, normalmente.
- Bloco de ancoragem de valor (head interno R$15-25k/mês) logo abaixo dos 3 cards, formato blockquote (mesma família visual de `.dor-quote`).
- Zero menção de R$ de plano/tier sobrevive, incluindo o "R$1.500" riscado que hoje aparece no card do Diagnóstico.

### `#garantia` — mesmo badge circular, corpo reescrito
Mantém `.garantia-badge` (90 — ainda verdadeiro, é a duração do ciclo). Corpo de texto substitui o mecanismo de devolução/mês grátis pela linguagem de risco compartilhado do brief (fee parcialmente variável, sem promessa de devolução). Lista de pré-condições (`.garantia-conditions`) mantém os 4 itens (ainda fazem sentido num modelo de risco compartilhado), só a frase final de consequência muda.

### `#fundadores` — sem mudança de conteúdo
Credenciais confirmadas pelo Murillo, mantidas como estão. Nenhuma correção necessária.

### `#faq` — 1 item reescrito
Item 1 ("Isso não é muito caro?") hoje cita "Sprint Ignição" por nome e usa "se paga com 2 novos pacientes". Reescreve pra tirar o nome do tier antigo e reforçar o modelo de risco compartilhado. O valor "R$2.000/mês" pode ser mantido (descreve uma agência concorrente hipotética, não é preço da Bäche).

### `#contato` / footer
- CTA final e sub-copy atualizados pra Raio-X.
- Footer, coluna "Serviços": troca links de Sprint Ignição/Retainer Presença/Programa Palco por links pros 3 planos novos + Raio-X gratuito.
- Footer, coluna "Empresa": "O Método Protagonista" → novo rótulo (mesmo `href="#metodo"`).

### JSON-LD (`<head>`)
`hasOfferCatalog.itemListElement` hoje lista as 4 ofertas antigas por nome. Atualiza pra Raio-X (mantém `price: 0`, é genuinamente gratuito) + 3 planos novos, sem campo de preço nos 3 (regra-mãe vale pra dados estruturados também). FAQPage do JSON-LD tem 6 perguntas diferentes das visíveis no acordeão — inconsistência pré-existente, fora do escopo deste brief; só ajusto a pergunta que cita explicitamente o modelo antigo, se houver.

## Dados/JS a atualizar

- **`P` array** (6 fases → vira `FRENTES`, 4 itens: Marca/Aquisição/Conversão/Retenção). Estrutura por item: papel, frase-cliente, dor de abertura, lista de entregáveis (cada um com etiqueta `faz`/`dirige`/`opera`), sinal. Marca ganha subseção Conteúdo.
- **`MOTOR` array** (novo, 4 itens): fase, quando, o que acontece.
- **`FQ_GAR`** (objeção → label interno, aparece no modal de qualificação): remapear:

| Objeção (mantém) | Label interno novo |
|---|---|
| Apareço igual a todo mundo | Marca |
| Travo na câmera / não apareço | Conteúdo |
| Anúncio traz paciente errado ou nenhum | Aquisição |
| Lead chega no WhatsApp e não fecha | Conversão |
| Não sei meu custo por paciente nem quanto ele vale | Régua do motor |
| Paciente não volta nem indica | Retenção |

- **Ring/hub math** (`metodoFw`): parametrizar de 6 nós fixos pra 4 (1 hub central clicável + 3 orbitando), mantendo o modo compacto mobile já existente.
- **CTA**: todo texto de botão (13 instâncias mapeadas) vira "Agendar meu Raio-X gratuito". `data-modal="diagnostico"` pode ficar como está internamente (não é visível ao usuário) ou renomear pra `raiox` — decisão de implementação, não afeta copy.

## Componentes reaproveitados (nenhum estilo novo inventado)

| Componente novo/mudado | Base reaproveitada |
|---|---|
| Etiqueta de responsabilidade (Bäche faz / Bäche dirige / Sua equipe opera) | `.pain-badge` (hoje 2 cores por modificador — crítica/alta), estendido pra 3 variantes |
| Diagrama mapa+flywheel | `metodoFw` (ring/hub SVG já existe, reduz de 6 pra 4 nós) |
| Painel de detalhe por frente | `.metodo-explorer` / `.mx-tab` / `.mx-panel` (rail desktop, acordeão mobile) |
| Coluna "quem executa" na tabela de diferenciais | `.check.yes` / `.check.no` (já existe) |
| Plano destacado (Ciclo completo) | `.product-card.featured` + `.product-badge` |
| Ancoragem de valor | Família visual de `.dor-quote` (blockquote) |
| Badge de garantia | `.garantia-badge` (mantém, só muda o texto ao redor) |

## Fora de escopo

`unit.html`, `painel_unit_economics_athlon.html` (arquivos avulsos, não fazem parte do site principal). `metodo-dirige-bache.md` e `index-framework.html` (exploração anterior descartada, confirmado). Faixas de faturamento em R$ no formulário de qualificação (descrevem o faturamento do cliente, não preço da Bäche — não são "preço de plano"). Sincronizar as 6 perguntas do FAQPage (JSON-LD) com as 6 visíveis no acordeão (inconsistência pré-existente, não introduzida por este trabalho).

## Checklist de aceite

Igual ao item 11 do brief original — repetido aqui pra virar critério de pronto da implementação:

- [ ] Identidade visual do site inalterada (paleta, fontes, componentes)
- [ ] Nenhuma menção a Método Protagonista ou às 6 fases antigas, em nenhum componente (incluindo JSON-LD)
- [ ] Mapa de 4 frentes + flywheel no lugar do método antigo
- [ ] Números tratados como régua do motor/infraestrutura de todo plano, nunca como quinta frente
- [ ] Motor de 90 dias (4 fases) presente e coerente
- [ ] Seção de entregáveis com etiqueta de responsabilidade em cada item
- [ ] Nenhum preço em reais em nenhum lugar do site (incluindo JSON-LD)
- [ ] 3 planos por abrangência, Ciclo completo destacado
- [ ] Bloco de ancoragem (head interno) presente, sem citar valor de plano
- [ ] Todos os CTAs apontam para o Raio-X gratuito
- [ ] Frente Conteúdo publicada integralmente (confirmado que a operação já existe)
- [ ] Estatísticas de precisão falsa arredondadas (291.362 / 41% / 25%)
- [ ] Credenciais do fundador mantidas como estão (confirmadas, sem mudança)
- [ ] Garantia suavizada para risco compartilhado, sem devolução de fee
- [ ] Glossário aplicado: sem jargão de marketing no texto voltado ao cliente
- [ ] Copy checada contra a tabela de pains/gains/JTBD, não só contra o glossário
