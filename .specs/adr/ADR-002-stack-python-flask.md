---
id: ADR-002
kind: adr
title: Usar Python com Flask e Jinja, pytest, Playwright e ruff para o catálogo local
parent: PROD-001
version: 1.0.1
status: accepted
date: 2026-10-28
deciders: [mdudagualberto]
related: [CONST-001, ADR-001, F-SETUP-V1, F-CATALOGO-V1]
supersedes: []
amends: []
last_updated: 2026-10-28
---

# ADR-002 — Stack do produto: Python + Flask/Jinja, pytest, Playwright, ruff

> Proposta preparada em 2026-10-28 a pedido da mantenedora. **G2 aceito em 2026-10-28** sobre a versão 1.0.0 (ver Revisões); Constitution §2 preenchida na versão 1.2.0.

## Contexto
O produto (PROD-001) é uma página local com lista de artigos fictícios, filtro por ano, contador, estado vazio e erro de entrada. A mantenedora prefere Python. O que mais pesa na escolha é o objetivo de aprendizado: cada AC precisa de um teste automatizado e determinístico, e a interface precisa permitir conferir teclado, foco e estados visuais com evidência persistente (AGENTS Regra 17). A tela só tem um formulário e uma lista, sem interatividade rica.

O Python 3 do tooling (biblioteca padrão) **não** é argumento: o tooling não obriga produto Python (ADR-001, Revisões). A escolha vem da preferência declarada e dos critérios abaixo.

Critérios, em ordem de peso:
1. Testar cada AC com pytest, sem rede e sem display, comparando o efeito observável (itens exibidos, contador, mensagens).
2. Controlar a semântica de acessibilidade: rótulo, `aria-invalid`, `aria-describedby`, foco após erro.
3. Exercitar teclado e capturar cada estado de forma reprodutível.
4. Poucas dependências e pouca infraestrutura para quem está aprendendo.

## Decisão
O produto é uma aplicação web local em **Python ≥ 3.10** (CI e desenvolvimento em 3.12), com **Flask 3.1** e templates **Jinja2** renderizados no servidor. Os dados ficam num **arquivo JSON local, somente leitura e versionado** (`data/artigos.json`), carregado e validado na inicialização. Testes com **pytest**; os testes de AC passam pelo cliente de teste do Flask e leem o HTML com **beautifulsoup4** (só em desenvolvimento). Teclado, foco e capturas por estado usam **Playwright para Python** (Chromium headless) em comando separado. **ruff** faz lint e checagem de formatação.

### Mecânica
- Estrutura: pacote `catalogo/` (`dados.py` carga/validação, `filtro.py` regra pura, `web.py` app factory e rota, `templates/`, `static/`), `tests/` (pytest), `tests/e2e/` (Playwright), `data/artigos.json`.
- Filtro via formulário `GET /` com os parâmetros `ano` (o texto digitado) e `aplicado` (último ano válido aplicado, em campo oculto). É isso que deixa o servidor preservar o resultado anterior quando a entrada é inválida, sem JavaScript.
- Servidor de desenvolvimento escuta só em `127.0.0.1`, sem modo debug. Sem banco, rede ou segredos.
- Dependências fixadas em versões exatas em `requirements.txt` (execução) e `requirements-dev.txt` (testes/lint/e2e), num `.venv` local (já ignorado no Git). As versões exatas entram no F-SETUP-V1, dentro das famílias desta ADR.

### Comandos do produto (implementados no F-SETUP-V1)
| Comando | Efeito | Rede? | Em `make check`? |
|---|---|---|---|
| `make app-setup` | Cria `.venv` e instala `requirements-dev.txt` | sim, uma vez (PyPI) | não |
| `make app-lint` | `ruff check catalogo tests` + `ruff format --check catalogo tests` | não | sim |
| `make app-test` | `python -m pytest tests --ignore=tests/e2e` | não | sim |
| `make e2e-setup` | `python -m playwright install chromium` | sim, uma vez | não |
| `make e2e` | `python -m pytest tests/e2e` (teclado/foco; capturas com `EVIDENCIA=1`) | não (só 127.0.0.1) | não |
| `make run` | `python -m catalogo` em http://127.0.0.1:5000 | não | não |
| `make check` | Checks do template (lint, drift, testes do tooling) + `app-lint` + `app-test` | não | — |

Build: não se aplica (Python interpretado). A prova de que a aplicação inicia é o teste de fumaça do F-SETUP-V1 (AC-1).

### Mudança proposta na Constitution §2 (aplicar só depois do G2, como bump minor 1.1.0 → 1.2.0)
| Camada | Decisão | ADR |
|---|---|---|
| Linguagem/runtime | Python ≥ 3.10 (CI 3.12) | ADR-002 |
| Framework | Flask 3.1 + Jinja2, renderização no servidor | ADR-002 |
| Persistência | Arquivo JSON local versionado, somente leitura | ADR-002 |
| Testes / lint | pytest 8 + beautifulsoup4; Playwright (e2e, comando separado) / ruff | ADR-002 |

## Consequências
- Positivas:
  - Toda AC de comportamento é testável com o cliente do Flask, em milissegundos, sem display nem rede.
  - O HTML é escrito por nós: rótulo, `aria-*`, ordem de foco e mensagens ficam sob controle e são verificáveis.
  - Playwright exercita o teclado de verdade e gera capturas por estado com dados de fixture.
  - O filtro funciona sem JavaScript (formulário nativo), o que simplifica teclado e testes.
- Negativas / o que se PERDE (registro honesto):
  - Cada filtro recarrega a página: o foco volta ao início, a não ser que o template o posicione (`autofocus` no erro), e não há anúncio dinâmico sem recarga.
  - Os testes e2e dependem de baixar o Chromium (~150 MB) uma vez e ficam fora do `make check` e da CI nesta fase, então teclado e foco não barram merge automaticamente.
  - Quatro dependências além do Flask só para desenvolvimento (pytest, beautifulsoup4, playwright e ruff).
  - Sem widgets prontos: a aparência fica por conta de um CSS mínimo próprio.

## Alternativas consideradas
| Critério | Flask + Jinja (escolhida) | Streamlit | Tkinter | `http.server` da biblioteca padrão |
|---|---|---|---|---|
| Testar ACs com pytest | Cliente de teste; HTML determinístico | `streamlit.testing.v1.AppTest` cobre widgets e textos, mas não o DOM final | Exige display (Xvfb na CI); estado lido nos widgets | Possível, mas roteamento e escaping escritos à mão |
| Semântica de acessibilidade | Total (HTML próprio) | Não define `aria-invalid`/`aria-describedby` nem foco após erro | Tk não expõe árvore de acessibilidade ao leitor de tela no Linux | Total, mas manual |
| Teclado e capturas | Playwright em navegador real | Playwright possível, com seletores gerados pelo framework (frágeis) | `event_generate` e captura de tela dependem do gerenciador de janelas | Playwright |
| Dependências | Flask (+ dev) | Streamlit traz pandas, pyarrow, tornado etc. | Nenhuma (stdlib) | Nenhuma |
| AC-5 (preservar resultado) | Campo oculto `aplicado` | `session_state` | Estado em memória | Campo oculto |

- **Streamlit** — rejeitada: a escrita da página é rápida, mas não temos controle sobre `aria-*` e foco, que são exatamente o que a feature precisa verificar. O modelo de reexecução esconde o fluxo, e as dependências são pesadas para uma lista de dez itens.
- **Tkinter** — rejeitada: não tem dependências, mas a acessibilidade com leitor de tela no Linux é fraca, os testes de UI exigem display e as capturas reproduzíveis dão mais trabalho.
- **`http.server` + `string.Template`** — rejeitada: evitar dependências obrigaria a reescrever roteamento, parsing de query e escaping de HTML. Seria criar um mini-framework (Regra 1) e aumentaria o risco de XSS.
- **Verificar teclado só manualmente, sem Playwright** — considerada como alternativa menor. Tem custo zero de dependência, mas a evidência de teclado deixa de ser reproduzível. Fica como plano B caso o download do navegador não seja aceitável (ver NEEDS_CLARIFICATION do F-SETUP-V1).

## Riscos
- `\d` e `str.isdigit()` em Python aceitam dígitos Unicode (por exemplo `٢٠٢٤`), o que violaria a regra “quatro dígitos de 0 a 9”. Mitigação: `re.fullmatch(r"[0-9]{4}", ...)` e caso de teste com dígitos não ASCII (F-CATALOGO-V1).
- O autoescape do Jinja vale para templates `.html`. Um título fictício com `&` ou um `ano` digitado com HTML precisa aparecer escapado. Mitigação: teste com entrada contendo marcação.
- O download do Chromium pode falhar em rede restrita. Mitigação: o comando é separado, e sem navegador o resultado é “não executado”, nunca verde.
- Atualizações de Flask ou Playwright fora das versões fixadas. Mitigação: pins exatos; atualização compatível entra em Revisões.

## Fences contra regressão
- `tests/test_arquitetura.py` (F-SETUP-V1 AC-4): módulos de domínio não importam Flask.
- `tests/test_comandos.py` (F-SETUP-V1 AC-3): `make check` falha quando um teste do produto falha.
- Constitution §2 preenchida com esta ADR. Trocar framework ou persistência exige ADR-002-v2 (`supersedes`) e bump major.
- Pins em `requirements*.txt` versionados; a CI instala exatamente essas versões.

## Revisões
- 2026-10-28: proposta inicial (in_review), aguardando G2.
- 2026-10-28: G2 — aceite da mantenedora em 2026-10-28 nesta conversa ("Revisei e aceito o produto, a stack e os contratos nestas versões"); não é aprovação final da entrega. Status accepted. Versão 1.0.1 corrige só a contagem de dependências em Consequências (três → quatro), sem mudar a decisão.
