---
id: TASKS-F-SETUP-V1
kind: tasks
title: Tarefas — F-SETUP-V1
parent: F-SETUP-V1
version: 0.1.0
status: approved
last_updated: 2026-10-28
---

# Tarefas

Uma task por comportamento ou grupo coeso. Toda task referencia AC; dependências formam uma ordem executável. A célula Status começa pelo estado real: todo, doing, blocked, done ou deferred. Um plano ou relato de agente não prova conclusão.

| ID | Descrição | AC | Depende de | Arquivos / responsável | Status | Evidência executada |
|---|---|---|---|---|---|---|
| T-000 | Reconciliar F-SDD-TOOLING-V1 AC-8 (teste de template intacto) com o bootstrap: spec do tooling primeiro, depois o teste, com contraprova | AC-3 | decisão Q-2 da mantenedora | .specs/features/F-SDD-TOOLING-V1/spec.md, scripts/tests/test_hooks.py / agente | done | 2026-10-28: AC-8 do tooling v0.2.0 + teste dos dois casos; contraprovas registradas em TASKS-F-SDD-TOOLING-V1 T-005; `make check`: 25 testes, 1 falha que seguia a regra nova até o G0 (Q-3); verde desde df98191. Estendido à §2 da Constitution no tooling v0.3.0 (TASKS-F-SDD-TOOLING-V1 T-006) |
| T-001 | Pins, pyproject e `make app-setup`; ambiente instalado | AC-1 | G2 + G1 | requirements*.txt, pyproject.toml, Makefile / agente | done | 2026-10-28: `.venv` criado com `make`-equivalente (`python3 -m venv` + pip, PyPI); `pip freeze` idêntico aos pins de requirements*.txt (diff vazio) |
| T-002 | Teste de fumaça vermelho → `create_app` e página mínima → verde | AC-1 | T-001 | tests/test_smoke.py, catalogo/web.py, catalogo/templates/ / agente | done | Vermelho: `pytest tests/test_smoke.py` → `ModuleNotFoundError: No module named 'catalogo'`. Verde: 1 passed. `make run`: 127.0.0.1:5000, Debug mode: off, h1 + 10 itens via curl |
| T-003 | Carga validada dos dados (casos válidos e inválidos, dígitos não ASCII) | AC-2 | T-001 | tests/test_dados.py, catalogo/dados.py, data/artigos.json, tests/fixtures/ / agente | done | Vermelho (com `ErroDados` vazio): 11 failed, 1 passed; `"２０２４"`/`"٢٠٢٤"` aceitos por `int()`. Verde: 12 passed. `data/artigos.json` (10 fictícios) carrega |
| T-004 | Teste de fronteira + contraprova com import proibido | AC-4 | T-002, T-003 | tests/test_arquitetura.py / agente | done | Passou de primeira (fronteira já respeitada). Contraprova em cópia: `import flask`, `from jinja2 import Template` e import dentro de função em dados.py → AssertionError citando DS-00 R1; controle 1 passed |
| T-005 | Alvos do produto no Makefile e `check` estendido | AC-3 | T-002 | Makefile / agente | done | `check` = `check-template` (checks originais, intactos) + `app-lint` + `app-test`; `make app-test VENV=/nao/existe` → mensagem “rode make app-setup”, exit 2 |
| T-006 | Teste de `make check` em cópia temporária (verde e com falha proposital) | AC-3 | T-005 | tests/test_comandos.py / agente | done | Vermelho antes do Makefile: `assert 0 != 0` (make check ignorava teste do produto). Verde depois: 1 passed em 18 s (cópia verde → 0; falha proposital → ≠0 com `FAILED tests/test_falha_proposital.py`) |
| T-007 | CI com Python 3.12, `app-setup` e `make check` | AC-3 | T-005 | .github/workflows/ci.yml / agente; resultado real depende de push (humano) | done | ci.yml: job `check` (template, 3.9, Linux+macOS) roda `make check-template`; job `product` (3.12, Linux) roda `make app-setup` + `make check`. CI real no commit 227ea63 (push feito pela mantenedora em 2026-10-29): run https://github.com/mdudagualberto/lab-sdd/actions/runs/40811044546 success; jobs product, check (ubuntu-24.04) e check (macos-latest) success |
| T-008 | Semente DS-00/06/07 com enforcement e exemplos reais | AC-4 | T-004, T-006 | .specs/design-system/ / agente | done | DS-00/06/07 com enforcement no mesmo commit; contraprovas em cópia: DS-00 R2 (`import json` em web.py), DS-06 R2 (teste usando DADOS_PADRAO), DS-07 R1 (ruff N802), DS-07 R2 (`tests/ajuda_extra.py`) falham; controle passa. N818 desligado com justificativa |
| T-009 | Correções da revisão independente (spec-reviewer, 2026-10-28) | AC-2, AC-3, AC-4 | T-008 | tests/test_dados.py, tests/test_comandos.py, tests/test_convencoes.py, DS-00/06/07 / agente | done | AC-2: mutante `$` + `match` sobrevivia; casos `"2024\n"`, `" 2024"`, `"2024 "` o derrubam. AC-3: venv = `sys.prefix`; marcador de cópia no lugar de variável (com `CATALOGO_TESTE_INTERNO=1` exportada o teste roda: 1 passed). DS-07 R1: ratchet do prefixo Erro (mutante `DadosError` falha). DS-00/06: linhas e escopo atualizados |

Antes de done: confira o diff, existência dos símbolos/arquivos e o resultado real. Uma tarefa parcialmente implementada fica doing; diferimento tem motivo, dono e tracking. Atualize esta tabela no commit da AC.
