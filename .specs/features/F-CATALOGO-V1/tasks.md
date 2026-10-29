---
id: TASKS-F-CATALOGO-V1
kind: tasks
title: Tarefas — F-CATALOGO-V1
parent: F-CATALOGO-V1
version: 0.1.0
status: approved
last_updated: 2026-10-28
---

# Tarefas

Uma task por comportamento ou grupo coeso. Toda task referencia AC; dependências formam uma ordem executável. A célula Status começa pelo estado real: todo, doing, blocked, done ou deferred. Um plano ou relato de agente não prova conclusão.

| ID | Descrição | AC | Depende de | Arquivos / responsável | Status | Evidência executada |
|---|---|---|---|---|---|---|
| T-001 | Fixture de 8 artigos e helpers de leitura do HTML | AC-1, AC-2 | F-SETUP-V1 concluída + G1 | tests/fixtures/artigos.json, tests/catalogo/conftest.py / agente | done | tests/catalogo/conftest.py (Pagina, abrir, oráculo `esperado` lendo a fixture); fixture de 8 artigos com 2024 ×3 não consecutivos (criada na F-SETUP-V1) |
| T-002 | Filtrar por ano e limpar filtro (vermelho → verde) | AC-1, AC-3 | T-001 | catalogo/filtro.py, catalogo/web.py, tests/catalogo/test_filtro_ano.py / agente | done | Vermelho 1 (sem marcação): `assert [] == [...]`. Vermelho 2 (marcação, sem filtro): 5 failed, 1 passed (`[8 títulos] == [3 de 2024]`). Verde: 6 passed |
| T-003 | Contador nos estados inicial, filtrado, vazio e erro | AC-2 | T-002 | catalogo/templates/catalogo.html, tests/catalogo/test_contador.py / agente | done | Vermelho: `assert None == 'Artigos exibidos: 8'` (contador inexistente). Verde: 7 passed nos 5 estados, inclusive após entrada inválida |
| T-004 | Lista vazia para ano válido sem artigos | AC-4 | T-002 | template, tests/catalogo/test_lista_vazia.py / agente | done | Vermelho: `assert None == 'Nenhum artigo encontrado'` (1999, 0000, 9999). Verde: 4 passed |
| T-005 | Erro de entrada, preservação do último filtro válido, remoção do erro; contraprova `\d` | AC-5, AC-6 | T-003 | catalogo/filtro.py, catalogo/web.py, tests/catalogo/test_entrada_invalida.py / agente | done | Vermelho: 18 failed (`assert None == 'Informe um ano com quatro dígitos'`); escape já passava (autoescape). Verde: 19 passed. Contraprova `\d{4}` em cópia: 5 casos não ASCII falham (filtro e carga) |
| T-006 | Marcação acessível do campo e do erro | AC-7 | T-005 | template, tests/catalogo/test_acessibilidade.py / agente | done | Vermelho: 2 failed (sem aria-invalid; sem #ajuda-ano). Verde: 4 passed |
| T-007 | Teclado e foco em navegador real | AC-8 | T-006, Q-1 | tests/e2e/ / agente | done | `make e2e`: 3 passed (Chromium headless 156, Playwright 1.64.1). Teste escrito depois do autofocus da AC-7, por isso passou de primeira; contraprova sem autofocus: `assert '' == 'ano'`, 1 failed |
| T-008 | Capturas por estado e variante, inspeção e registro no design.md | AC-1, AC-2, AC-4, AC-5, AC-7 | T-007 | docs/images/, design.md / agente (captura) + mantenedora (revisão visual) | done | `EVIDENCIA=1 make e2e`: 10 capturas em docs/images/ (commit 0e41e52), abertas e inspecionadas pelo agente e registradas no design.md; contraste AA calculado. Revisão visual humana: a mantenedora informou em 2026-10-28 que viu e aprovou as imagens |
| T-009 | Verificação com leitor de tela real | AC-7 | T-008 | design.md / mantenedora | deferred | fora da V1; dona: mantenedora |
| T-010 | Correções da revisão independente (spec-reviewer, 2026-10-28, APROVAR COM RESSALVAS) | AC-1, AC-5 | T-008 | catalogo/templates/catalogo.html, tests/catalogo/ / agente | done | Achado 1: `0999`/`0000` exibidos como `999`/`0`; vermelho reproduzido (2 failed), corrigido com `"%04d" \| format`, verde. Achado 3: mutante `\| safe` no título sobrevivia; novo teste de escape de título e autores o derruba (1 failed no mutante, verde no código) |

Antes de done: confira o diff, existência dos símbolos/arquivos e o resultado real. Uma tarefa parcialmente implementada fica doing; diferimento tem motivo, dono e tracking. Atualize esta tabela no commit da AC.
