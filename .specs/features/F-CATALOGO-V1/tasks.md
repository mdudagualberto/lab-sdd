---
id: TASKS-F-CATALOGO-V1
kind: tasks
title: Tarefas — F-CATALOGO-V1
parent: F-CATALOGO-V1
version: 0.1.0
status: in_review
last_updated: 2026-10-28
---

# Tarefas

Uma task por comportamento ou grupo coeso. Toda task referencia AC; dependências formam uma ordem executável. A célula Status começa pelo estado real: todo, doing, blocked, done ou deferred. Um plano ou relato de agente não prova conclusão.

| ID | Descrição | AC | Depende de | Arquivos / responsável | Status | Evidência executada |
|---|---|---|---|---|---|---|
| T-001 | Fixture de 8 artigos e helpers de leitura do HTML | AC-1, AC-2 | F-SETUP-V1 concluída + G1 | tests/fixtures/artigos.json, tests/catalogo/conftest.py / agente | blocked | aguardando G1 e F-SETUP-V1 |
| T-002 | Filtrar por ano e limpar filtro (vermelho → verde) | AC-1, AC-3 | T-001 | catalogo/filtro.py, catalogo/web.py, tests/catalogo/test_filtro_ano.py / agente | todo | — |
| T-003 | Contador nos estados inicial, filtrado, vazio e erro | AC-2 | T-002 | catalogo/templates/catalogo.html, tests/catalogo/test_contador.py / agente | todo | — |
| T-004 | Lista vazia para ano válido sem artigos | AC-4 | T-002 | template, tests/catalogo/test_lista_vazia.py / agente | todo | — |
| T-005 | Erro de entrada, preservação do último filtro válido, remoção do erro; contraprova `\d` | AC-5, AC-6 | T-003 | catalogo/filtro.py, catalogo/web.py, tests/catalogo/test_entrada_invalida.py / agente | todo | — |
| T-006 | Marcação acessível do campo e do erro | AC-7 | T-005 | template, tests/catalogo/test_acessibilidade.py / agente | todo | — |
| T-007 | Teclado e foco em navegador real | AC-8 | T-006, Q-1 | tests/e2e/ / agente | todo | — |
| T-008 | Capturas por estado e variante, inspeção e registro no design.md | AC-1, AC-2, AC-4, AC-5, AC-7 | T-007 | docs/images/, design.md / agente (captura) + mantenedora (revisão visual) | todo | — |
| T-009 | Verificação com leitor de tela real | AC-7 | T-008 | design.md / mantenedora | deferred | fora da V1; dona: mantenedora |

Antes de done: confira o diff, existência dos símbolos/arquivos e o resultado real. Uma tarefa parcialmente implementada fica doing; diferimento tem motivo, dono e tracking. Atualize esta tabela no commit da AC.
