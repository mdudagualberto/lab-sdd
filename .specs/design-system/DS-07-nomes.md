---
id: DS-07-nomes
kind: design_system_spec
title: Design System §7 — Nomes no catálogo
parent: CONST-001
version: 1.0.0
status: in_review
owners: [mdudagualberto]
related_adrs: [ADR-002]
last_updated: 2026-10-28
spec_hash: pending
status_history:
  - { version: 1.0.0, status: in_review, date: 2026-10-28, note: "semente (F-SETUP-V1), descreve o esqueleto existente" }
---

# Design System §7 — Nomes

> **Normativo** (AGENTS.md Regra 13). Snapshot do que o código JÁ faz; obrigatório dali em diante. Desvio exige ADR.

## Escopo
Nomes de módulos, funções, classes e arquivos de teste do produto, e mensagens de commit. Observação descritiva, sem regra: o domínio é nomeado em português (`carregar_artigos`, `Artigo`, `ErroDados`), porque nenhum lint verifica idioma.

## Regras
1. **R1 —** Funções, variáveis e módulos usam `snake_case`; classes usam `PascalCase`; exceções do domínio usam o prefixo `Erro` (não o sufixo inglês `Error`).
2. **R2 —** Arquivos de teste se chamam `test_*.py`; só `conftest.py` e `__init__.py` fogem disso.
3. **R3 —** Mensagens de commit seguem Conventional Commits.

## Enforcement
| Regra | Como é cobrada | Onde |
|---|---|---|
| R1 | ruff `N` (pep8-naming), com N818 desligado e justificado | `pyproject.toml:12-14` |
| R2 | Ratchet sobre `tests/` (contraprova: `tests/ajuda_extra.py`) | `tests/test_convencoes.py::test_arquivos_de_teste_seguem_test_prefixo` |
| R3 | Hook Git commit-msg do template | `scripts/sdd/git-commit-msg.sh` |

Regra sem linha nesta tabela é folclore — não a escreva.

## Exemplos canônicos
- `catalogo/dados.py:11` — `class ErroDados(ValueError)`: prefixo `Erro`.
- `catalogo/dados.py:16` e `catalogo/dados.py:22` — `class Artigo` e `def carregar_artigos`.
- `tests/test_dados.py:20` — `test_carrega_artigos_validos_na_ordem_do_arquivo`: o nome descreve o comportamento.

## Anti-padrões
- Renomear `ErroDados` para `DadosError` só para agradar o N818: mistura idiomas no mesmo nome.

## Changelog
- 1.0.0 (2026-10-28): semente.
