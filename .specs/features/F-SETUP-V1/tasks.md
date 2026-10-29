---
id: TASKS-F-SETUP-V1
kind: tasks
title: Tarefas — F-SETUP-V1
parent: F-SETUP-V1
version: 0.1.0
status: in_review
last_updated: 2026-10-28
---

# Tarefas

Uma task por comportamento ou grupo coeso. Toda task referencia AC; dependências formam uma ordem executável. A célula Status começa pelo estado real: todo, doing, blocked, done ou deferred. Um plano ou relato de agente não prova conclusão.

| ID | Descrição | AC | Depende de | Arquivos / responsável | Status | Evidência executada |
|---|---|---|---|---|---|---|
| T-000 | Reconciliar F-SDD-TOOLING-V1 AC-8 (teste de template intacto) com o bootstrap: spec do tooling primeiro, depois o teste, com contraprova | AC-3 | decisão Q-2 da mantenedora | .specs/features/F-SDD-TOOLING-V1/spec.md, scripts/tests/test_hooks.py / agente | done | 2026-10-28: AC-8 do tooling v0.2.0 + teste dos dois casos; contraprovas registradas em TASKS-F-SDD-TOOLING-V1 T-005; `make check`: 25 testes, 1 falha que segue a regra nova (Q-3). Estendido à §2 da Constitution no tooling v0.3.0 (TASKS-F-SDD-TOOLING-V1 T-006) |
| T-001 | Pins, pyproject e `make app-setup`; ambiente instalado | AC-1 | G2 + G1 | requirements*.txt, pyproject.toml, Makefile / agente | blocked | aguardando G1/G2 |
| T-002 | Teste de fumaça vermelho → `create_app` e página mínima → verde | AC-1 | T-001 | tests/test_smoke.py, catalogo/web.py, catalogo/templates/ / agente | todo | — |
| T-003 | Carga validada dos dados (casos válidos e inválidos, dígitos não ASCII) | AC-2 | T-001 | tests/test_dados.py, catalogo/dados.py, data/artigos.json, tests/fixtures/ / agente | todo | — |
| T-004 | Teste de fronteira + contraprova com import proibido | AC-4 | T-002, T-003 | tests/test_arquitetura.py / agente | todo | — |
| T-005 | Alvos do produto no Makefile e `check` estendido | AC-3 | T-002 | Makefile / agente | todo | — |
| T-006 | Teste de `make check` em cópia temporária (verde e com falha proposital) | AC-3 | T-005 | tests/test_comandos.py / agente | todo | — |
| T-007 | CI com Python 3.12, `app-setup` e `make check` | AC-3 | T-005 | .github/workflows/ci.yml / agente; resultado real depende de push (humano) | todo | — |
| T-008 | Semente DS-00/06/07 com enforcement e exemplos reais | AC-4 | T-004, T-006 | .specs/design-system/ / agente | todo | — |

Antes de done: confira o diff, existência dos símbolos/arquivos e o resultado real. Uma tarefa parcialmente implementada fica doing; diferimento tem motivo, dono e tracking. Atualize esta tabela no commit da AC.
