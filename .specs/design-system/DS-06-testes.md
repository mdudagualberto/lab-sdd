---
id: DS-06-testes
kind: design_system_spec
title: Design System §6 — Testes do catálogo
parent: CONST-001
version: 1.0.1
status: in_review
owners: [mdudagualberto]
related_adrs: [ADR-002]
last_updated: 2026-10-28
spec_hash: pending
status_history:
  - { version: 1.0.0, status: in_review, date: 2026-10-28, note: "semente (F-SETUP-V1), descreve o esqueleto existente" }
  - { version: 1.0.1, status: in_review, date: 2026-10-28, note: "R5 com marcador de cópia em vez de variável de ambiente; linhas atualizadas (achados da revisão independente (spec-reviewer) de 2026-10-28)" }
---

# Design System §6 — Testes

> **Normativo** (AGENTS.md Regra 13). Snapshot do que o código JÁ faz; obrigatório dali em diante. Desvio exige ADR.

## Escopo
Testes do produto em `tests/` (pytest). Fora do escopo: testes do tooling em `scripts/tests/` (unittest, F-SDD-TOOLING-V1).

## Regras
1. **R1 —** Testes do produto ficam em `tests/` e rodam com `make app-test`, dentro do `make check`; testes de navegador ficam em `tests/e2e/` e rodam só com `make e2e`.
2. **R2 —** Testes de comportamento usam os dados de `tests/fixtures/artigos.json` pela fixture `app`, nunca `data/artigos.json` nem `DADOS_PADRAO`.
3. **R3 —** A fixture `app` depende de `sem_rede`: qualquer conexão de rede durante o teste falha.
4. **R4 —** Toda AC aponta, por `@test:`, para o arquivo de teste que a cobre.
5. **R5 —** `make check` reprova quando um teste do produto falha.

## Enforcement
| Regra | Como é cobrada | Onde |
|---|---|---|
| R1 | `testpaths` do pytest e `--ignore=tests/e2e` no alvo `app-test`; `check` depende de `app-test` | `pyproject.toml:17`, `Makefile:40-41` |
| R2 | Ratchet que procura `data/artigos.json`/`DADOS_PADRAO` nos testes (contraprova: arquivo de teste importando `DADOS_PADRAO`) | `tests/test_convencoes.py::test_testes_nao_usam_dados_de_demonstracao` |
| R3 | Fixture `sem_rede` substitui `socket.connect` e `socket.create_connection`; `app` a requer | `tests/conftest.py:10`, `tests/conftest.py:21` |
| R4 | spec-lint R3 (formato) e R5 (arquivo existe em approved) | `scripts/sdd/sdd.py` (lint) |
| R5 | Teste que roda `make check` numa cópia com uma falha proposital, usando o venv da própria suíte (`sys.prefix`); só pula na cópia, que tem o marcador `.catalogo-teste-interno` | `tests/test_comandos.py::test_make_check_verde_e_vermelho_com_teste_do_produto` |

Regra sem linha nesta tabela é folclore — não a escreva.

## Exemplos canônicos
- `tests/conftest.py:6` e `tests/conftest.py:24` — `FIXTURE` e `create_app(FIXTURE)`.
- `tests/test_dados.py:52` — teste parametrizado com casos de erro, inclusive dígitos não ASCII.
- `tests/test_comandos.py:48` — teste de comando com contraprova embutida (verde e depois vermelho).

## Anti-padrões
- Testar a regra de ano só com dígitos ASCII: `int("２０２４")` funciona em Python e esconde o defeito (visto no vermelho da AC-2 em 2026-10-28).
- Declarar uma AC coberta porque o arquivo existe: o vínculo `@test:` não executa nada.

## Changelog
- 1.0.0 (2026-10-28): semente.
- 1.0.1 (2026-10-28): R5 deixa de depender de variável de ambiente (exportá-la pulava o controle em silêncio); linhas atualizadas.
