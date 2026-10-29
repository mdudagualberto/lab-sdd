---
id: TASKS-F-SDD-TOOLING-V1
kind: tasks
title: Tarefas de evolução do tooling
parent: F-SDD-TOOLING-V1
version: 0.3.0
status: in_review
last_updated: 2026-10-28
---

| ID | Descrição | AC | Status | Evidência |
|---|---|---|---|---|
| T-001 | Setup e Git verificam o conteúdo efetivo | AC-1, AC-6 | done | scripts/tests/test_tooling.py |
| T-002 | Índice e lint determinísticos | AC-2, AC-7 | done | scripts/tests/test_tooling.py |
| T-003 | Guards e ciclo de sessão com contrato testado | AC-3, AC-4, AC-5 | done | scripts/tests/test_hooks.py |
| T-004 | Templates e relato de aprendizados sem dados de produto | AC-7, AC-8 | done | docs/learned-practices.md |
| T-005 | Invariante de PROD-001 segue o estado do bootstrap (pending exige “Produto a definir”; complete proíbe; outro valor falha) | AC-8 | done | 2026-10-28, commit df98191: `scripts/tests/test_hooks.py` (`bootstrap_problem` + `test_bootstrap_placeholder_follows_bootstrap_state`). Contraprovas em cópia da árvore: controle OK; `sempre_none`, `regra_antiga` e `invalido_aceito` falham por AssertionError. `make check`: no dia, 1 falha esperada enquanto PROD-001 estava em pending; depois do G0 (df98191), 25 testes OK. Revisão independente (spec-reviewer, 2026-10-28): leu o código; não executou em Python 3.9 |
| T-006 | Mesma regra para a §2 da Constitution (pending exige “a definir no bootstrap”, complete proíbe; histórico fora da §2 ignorado) | AC-8 | done | 2026-10-28, commit df98191: `bootstrap_problem(product, constitution)` e casos sintéticos em `test_bootstrap_placeholder_follows_bootstrap_state`. Contraprovas em cópia da árvore: controle OK; `ignora_constituicao`, `arquivo_inteiro`, `ignora_prod` e `aceita_invalido` falham por AssertionError (a última passava na primeira versão do teste, que foi reforçado). `make check`: 1 falha conhecida até o G0; 25 testes OK depois do G0. Revisão independente (spec-reviewer, 2026-10-28): sem achado no tooling |

Validação do integrador em 2026-10-26: make check (24 testes), make test-mutations (4 contraprovas), make doctor e revisão adversarial independente após correções. Smoke automático do Claude e CI remota são limites registrados no postmortem.
