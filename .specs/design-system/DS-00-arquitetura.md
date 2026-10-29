---
id: DS-00-arquitetura
kind: design_system_spec
title: Design System §0 — Arquitetura e fronteiras do catálogo
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

# Design System §0 — Arquitetura e fronteiras

> **Normativo** (AGENTS.md Regra 13). Snapshot do que o código JÁ faz; obrigatório dali em diante. Desvio exige ADR.

## Escopo
Fronteiras dentro do pacote `catalogo/`: o domínio (`dados.py`, futuramente `filtro.py`) e a camada web (`web.py`, `__main__.py`, `templates/`). Fora do escopo: CSS e aparência (design.md) e o tooling SDD em `scripts/`.

## Regras
1. **R1 —** Só `catalogo/web.py` e `catalogo/__main__.py` importam `flask` ou `jinja2`; o restante do pacote é Python puro.
2. **R2 —** Só `catalogo/dados.py` importa `json`: o formato dos artigos tem uma fonte única (`carregar_artigos`), e os outros módulos recebem `Artigo`.

## Enforcement
| Regra | Como é cobrada | Onde |
|---|---|---|
| R1 | Teste que varre imports com `ast` e falha citando DS-00 R1 (contraprova: `import flask`, `from jinja2 import ...` e import dentro de função em `dados.py` derrubam o teste) | `tests/test_arquitetura.py::test_dominio_nao_importa_flask_nem_jinja` |
| R2 | Teste que varre imports com `ast` e falha citando DS-00 R2 (contraprova: `import json` em `web.py`) | `tests/test_arquitetura.py::test_so_dados_le_o_formato_json` |

Regra sem linha nesta tabela é folclore — não a escreva.

## Exemplos canônicos
- `catalogo/web.py:5` — `from flask import Flask, render_template`: o único ponto de entrada de Flask.
- `catalogo/web.py:7` — a camada web importa o domínio (`from catalogo.dados import carregar_artigos`); o domínio nunca importa a web.
- `catalogo/web.py:12` — `create_app(caminho_dados=None)`: factory que recebe o caminho dos dados, o que permite testar com fixture.
- `catalogo/dados.py:22` e `catalogo/dados.py:24` — `carregar_artigos` é o único `json.loads` do pacote.
- `tests/test_arquitetura.py:7` — `CAMADA_WEB = {"web.py", "__main__.py"}`: a lista explícita da fronteira.

## Anti-padrões
- Ler `data/artigos.json` direto na rota ou no template: duplica o formato e pula a validação (ver F-SETUP-V1 AC-2).
- Regra de filtro dentro da view: fica impossível testar sem Flask, e a F-CATALOGO-V1 exige `filtro.py` puro.

## Changelog
- 1.0.0 (2026-10-28): semente.
