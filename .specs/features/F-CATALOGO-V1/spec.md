---
id: F-CATALOGO-V1
kind: feature_spec
title: Catálogo de artigos com filtro por ano, contador, lista vazia e erro de entrada
parent: PROD-001
version: 0.1.2
status: in_review
risk_tier: minimal
data_classification: public
slo: {}
issue: none
owners: [mdudagualberto]
deps: [F-SETUP-V1]
related_adrs: [ADR-002]
last_updated: 2026-10-28
spec_hash: pending
status_history:
  - { version: 0.1.0, status: draft, date: 2026-10-28, note: "proposta a partir dos critérios AC-1..AC-5 da seção 4 do guia pós-aula, com decisões de comportamento registradas; aguarda G1 da mantenedora" }
  - { version: 0.1.1, status: draft, date: 2026-10-28, note: "NEEDS_CLARIFICATION: lápide da Q-1 (Playwright aceito pela mantenedora; AC-8 mantida, verificada por make e2e); sem mudança de AC; gates ainda não aceitos" }
  - { version: 0.1.1, status: in_review, date: 2026-10-28, note: "G1 sobre a versão 0.1.1: aceite da mantenedora em 2026-10-28 nesta conversa ("Revisei e aceito o produto, a stack e os contratos nestas versões"); não é aprovação final da entrega; implementação local autorizada" }
  - { version: 0.1.2, status: in_review, date: 2026-10-28, note: "D-4 registra que o ano é sempre exibido com quatro dígitos (0999, 0000). O código e o teste já existiam desde 49a4403, após achado da revisão independente; a spec não dizia como o ano é exibido (spec gap (a) do PM-catalogo-bootstrap-2026-10-28). Pedido da mantenedora; sem AC nova; não é aprovação final" }
---

# F-CATALOGO-V1 — Catálogo com filtro por ano

> O grupo de estudos quer ver quais artigos são de um ano e quantos são. Ponto de partida: história #42 do Portal de Pesquisa e os critérios propostos no guia pós-aula (seção 4), adotados aqui com as decisões abaixo.

## WHAT/HOW
### WHAT
A página inicial lista os artigos fictícios (título, autores, ano) com um contador. A pessoa digita um ano e aplica o filtro pelo botão ou pela tecla Enter. A lista e o contador passam a mostrar só os artigos daquele ano. Um ano sem artigos mostra uma mensagem de lista vazia. Uma entrada inválida mostra um erro e mantém na tela o resultado que já estava lá.

### HOW
```
GET /?ano=TEXTO&aplicado=AAAA
        │
        ▼
catalogo/web.py ── interpretar_entrada(ano) ──▶ catalogo/filtro.py (puro, sem Flask)
        │            ├─ vazio após strip      → filtro = nenhum (todos)
        │            ├─ fullmatch [0-9]{4}    → filtro = ano
        │            └─ outro                 → erro; filtro = interpretar(aplicado) ou nenhum
        │          filtrar(artigos, filtro) → lista na ordem do arquivo
        ▼
templates/catalogo.html: formulário (campo "ano", oculto "aplicado" = último ano válido),
contador, lista ou "Nenhum artigo encontrado", mensagem de erro quando houver
```
- `filtro.py` expõe funções puras (`interpretar_entrada`, `filtrar`). `web.py` só traduz a query string para essas funções e as funções para o template.
- O campo oculto `aplicado` guarda o último filtro válido efetivamente aplicado (vazio = todos). É essa a definição de “resultado anterior” da AC-5.

### Decisões de comportamento (registradas a pedido da mantenedora)
| ID | Decisão | Origem |
|---|---|---|
| D-1 | Estado inicial (`GET /` sem parâmetros): todos os artigos, sem erro, campo vazio | proposta; consistente com AC-3 do guia |
| D-2 | Ordem da lista: a mesma do arquivo de dados, sem reordenar (vale para todos os estados) | proposta; Regra 4 (menor solução) |
| D-3 | Entrada normalizada com `str.strip()` do Python (espaços, tabulação e quebras de linha nas pontas). Vazia após strip = “sem filtro” (AC-3), não é erro | guia AC-5 + proposta |
| D-4 | Ano válido = exatamente quatro caracteres de `0` a `9` (ASCII), sem faixa mínima ou máxima: `0000` e `9999` são válidos e caem em lista vazia. O ano de cada artigo é sempre exibido com quatro dígitos, com zeros à esquerda (`0999`, não `999`), coberto por `tests/catalogo/test_filtro_ano.py::test_ac1_ano_exibido_mantem_quatro_digitos` | guia AC-5; sem faixa por Regra 4; exibição: revisão 0.1.2 |
| D-5 | Dígitos não ASCII (`２０２４`, `٢٠٢٤`), sinais (`+2024`), espaços internos (`20 24`) e decimais (`2024.0`) são entrada inválida | consequência de D-4 |
| D-6 | “Resultado anterior” na AC-5 = resultado do último filtro válido aplicado, carregado no campo `aplicado`. Se `aplicado` estiver ausente ou inválido (URL editada à mão), vale “todos” | proposta; resolve como o servidor sem estado preserva a tela |
| D-7 | Com erro, o campo mantém o texto digitado (para correção), recebe foco ao carregar a página e é marcado como inválido | proposta; guia pede definir como o erro aparece |
| D-8 | O erro desaparece na próxima aplicação com entrada válida ou vazia; não há validação enquanto se digita | proposta; guia pede definir como o erro desaparece |
| D-9 | Contador com texto fixo “Artigos exibidos: N” (sem plural), igual ao número de itens visíveis | proposta; evita regra de plural |
| D-10 | Não há botão “Limpar” na V1: limpar = esvaziar o campo e aplicar (Enter ou Filtrar) | guia AC-3; Regra 4 |
| D-11 | Aplicação do filtro por teclado: Enter no campo envia o formulário (comportamento nativo); ordem de Tab: campo Ano → botão Filtrar | proposta; guia pede definir teclado |
| D-12 | Toda saída é escapada pelo autoescape do Jinja; texto digitado com marcação aparece literalmente | Constitution §3 (entrada validada na borda) |

## User Stories
- **US-1.** Como membro do grupo, quero filtrar os artigos por ano de publicação, para encontrar os de um ano específico.
- **US-2.** Como membro do grupo, quero ver quantos artigos estão na tela, para saber o tamanho do resultado sem contar.
- **US-3.** Como membro do grupo, quero ser avisado quando digito um ano inválido sem perder o que já estava filtrado, para corrigir sem recomeçar.
- **US-4.** Como pessoa que usa só o teclado, quero aplicar o filtro e chegar ao erro sem mouse, para usar o catálogo com a mesma eficiência.

## Acceptance Criteria
- **AC-1.** Ao aplicar o ano 2024, a lista mostra todos e somente os artigos de 2024 do conjunto de dados, na ordem do arquivo; com espaços nas pontas (" 2024 ") o resultado é o mesmo. @test:tests/catalogo/test_filtro_ano.py
- **AC-2.** O contador mostra “Artigos exibidos: N”, com N igual à quantidade de artigos visíveis, no estado inicial, filtrado, sem resultados e após entrada inválida. @test:tests/catalogo/test_contador.py
- **AC-3.** Ao aplicar o filtro com o campo vazio ou só com espaços, inclusive depois de um filtro por ano, a lista volta a mostrar todos os artigos do conjunto, na ordem do arquivo. @test:tests/catalogo/test_filtro_ano.py
- **AC-4.** Um ano válido sem artigos (por exemplo 1999 ou 0000) mostra “Nenhum artigo encontrado”, nenhum item de lista e “Artigos exibidos: 0”. @test:tests/catalogo/test_lista_vazia.py
- **AC-5.** Entrada não vazia que, após strip, não tenha exatamente quatro dígitos de 0 a 9 (texto, três ou cinco dígitos, dígitos não ASCII, sinal, espaço interno) mostra “Informe um ano com quatro dígitos”, mantém a lista e o contador do último filtro válido aplicado e mantém o texto digitado no campo. @test:tests/catalogo/test_entrada_invalida.py
- **AC-6.** Depois de um erro, aplicar um ano válido ou o campo vazio remove a mensagem de erro e mostra o resultado correspondente. @test:tests/catalogo/test_entrada_invalida.py
- **AC-7.** O campo tem rótulo visível “Ano de publicação” associado; no estado de erro, o campo tem aria-invalid="true", autofocus e aria-describedby apontando para o elemento da mensagem; fora do erro, não tem aria-invalid nem mensagem. @test:tests/catalogo/test_acessibilidade.py
- **AC-8.** Num navegador real, a partir do topo da página, Tab leva ao campo Ano e depois ao botão Filtrar; digitar 2024 e pressionar Enter aplica o filtro; após uma entrada inválida enviada com Enter, o foco está no campo Ano. @test:tests/e2e/test_teclado.py

## Risks
Resumo em risks.md: dígitos Unicode aceitos por `\d`/`isdigit`, `aplicado` adulterado na URL, perda de foco no recarregamento, escape de HTML e e2e fora da CI.

## Out of scope
- Intervalo de anos (próxima revisão; seção 9 do guia).
- Filtro por autor, título ou busca textual; ordenação configurável; paginação.
- Validação enquanto se digita, JavaScript no cliente, botão Limpar.
- Anúncio por leitor de tela verificado com tecnologia assistiva real (só a marcação é testada; ver design.md).
- Login, rede, banco remoto, deploy e exportação BibTeX (PROD-001 §8).

## NFRs
Herdados da Constitution §3. Erro de entrada tem um único texto documentado (AC-5). A suíte de AC-1..AC-7 é hermética (cliente do Flask, fixture `tests/fixtures/artigos.json`). AC-8 roda em `make e2e`, fora do `make check` (ADR-002). Overrides: nenhum.

## NEEDS_CLARIFICATION
- nenhum. ~~Q-1~~ (lápide, 2026-10-28): Playwright aceito pela mantenedora; AC-8 mantida, verificada por `make e2e` antes da entrega.
