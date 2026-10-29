---
id: F-SETUP-V1
kind: feature_spec
title: Esqueleto Python/Flask do catálogo com dados fictícios, testes, lint e CI
parent: PROD-001
version: 0.2.0
status: in_review
risk_tier: minimal
data_classification: public
slo: {}
issue: none
owners: [mdudagualberto]
deps: []
related_adrs: [ADR-002]
last_updated: 2026-10-28
spec_hash: pending
status_history:
  - { version: 0.1.0, status: draft, date: 2026-10-28, note: "proposta do bootstrap; depende do G2 da ADR-002; aguarda G1 da mantenedora" }
  - { version: 0.1.1, status: draft, date: 2026-10-28, note: "Q-1 e Q-2 respondidas pela mantenedora; Q-3 aberta; gates ainda não aceitos" }
  - { version: 0.2.0, status: draft, date: 2026-10-28, note: "AC-2: ano só como string de quatro dígitos ASCII, convertida para int depois da validação (antes também aceitava inteiro 1000–9999, o que era inconsistente); resumo de Risks alinhado ao risks.md; Q-3 resolvida pela mantenedora (opção a); gates ainda não aceitos" }
  - { version: 0.2.0, status: in_review, date: 2026-10-28, note: "G1 sobre a versão 0.2.0: aceite da mantenedora em 2026-10-28 nesta conversa ("Revisei e aceito o produto, a stack e os contratos nestas versões"); não é aprovação final da entrega; implementação local autorizada" }
---

# F-SETUP-V1 — Esqueleto do produto

> O catálogo ainda não tem código. Esta feature cria o menor esqueleto que prova a stack da ADR-002: a app sobe, os dados fictícios carregam validados, os testes e o lint do produto entram no `make check` e na CI, e a semente DS-00/06/07 passa a descrever o que existe.

## WHAT/HOW
### WHAT
Quem clona o repositório consegue instalar o ambiente do produto, rodar a página local com dados fictícios e verificar tudo com um único `make check`, que agora inclui testes e lint da aplicação.

### HOW
```
data/artigos.json ──▶ catalogo/dados.py ──▶ catalogo/web.py (create_app, GET /) ──▶ templates/catalogo.html
   (fictício)          carregar_artigos()      Flask; única camada que importa Flask
                       valida e lança ErroDados
tests/ (pytest, cliente do Flask; fixture tests/fixtures/artigos.json)
tests/e2e/ (Playwright; comando separado)
```
- `create_app(caminho_dados=None)`: sem argumento, usa `data/artigos.json`; os testes passam uma fixture própria (não dependem dos dados de demonstração).
- `carregar_artigos(caminho)` devolve `list[Artigo]` (dataclass imutável: `titulo: str`, `autores: tuple[str, ...]`, `ano: int`) na ordem do arquivo. Formato: lista JSON de objetos `{"titulo": str, "autores": [str, ...], "ano": "AAAA"}` em que `ano` precisa ser uma string JSON de exatamente quatro dígitos ASCII (`[0-9]{4}`, a mesma regra da entrada na F-CATALOGO-V1), convertida para `int` só depois da validação. Inteiro JSON (`2024`), dígitos não ASCII e outros tamanhos são inválidos. Registro inválido ou JSON malformado lança `ErroDados` com o índice do registro e o campo. A app não sobe com dados inválidos.
- Neste esqueleto, a página mostra só o título “Catálogo de artigos” e a lista sem filtro. O filtro, o contador e os estados são da F-CATALOGO-V1.
- `python -m catalogo` sobe em 127.0.0.1:5000, sem debug.
- Comandos, `.venv`, pins e CI conforme ADR-002 (§Comandos do produto). `make check` passa a executar `app-lint` e `app-test` depois dos checks do template.
- A CI (`.github/workflows/ci.yml`) ganha setup do Python 3.12, `make app-setup` e `make check`. O e2e fica fora da CI nesta versão.
- Semente DS-00 (fronteiras: domínio sem Flask), DS-06 (testes: pytest, fixture própria, cliente do Flask, e2e separado) e DS-07 (nomes: módulos e identificadores de domínio em português, `snake_case`, testes `test_*.py`), escritas depois do código existir, cada uma com enforcement.

## User Stories
- **US-1.** Como mantenedora, quero um esqueleto que sobe e é testado por um comando, para implementar a feature de usuário por AC com teste vermelho → verde.
- **US-2.** Como revisor(a), quero que `make check` e a CI falhem quando um teste do produto falha, para que verde signifique algo sobre o produto e não só sobre as specs.

## Acceptance Criteria
- **AC-1.** `create_app()` com a fixture de dados responde `GET /` com status 200 e um `h1` com o texto exato “Catálogo de artigos”, sem acesso à rede. @test:tests/test_smoke.py
- **AC-2.** `carregar_artigos` devolve os artigos válidos na ordem do arquivo; JSON malformado, campo ausente, autores vazio e ano que não seja string de exatamente quatro dígitos ASCII (inclusive inteiro JSON) lançam `ErroDados` com o índice do registro e o campo, e `create_app` não inicia com esses dados. @test:tests/test_dados.py
- **AC-3.** Numa cópia temporária do repositório, `make check` termina com código 0 no estado atual e com código diferente de 0 quando se acrescenta um teste do produto que falha. @test:tests/test_comandos.py
- **AC-4.** Nenhum módulo de `catalogo/` além de `web.py` e `__main__.py` importa `flask` ou `jinja2`, e o teste falha, citando DS-00, quando essa fronteira é violada. @test:tests/test_arquitetura.py

## Risks
Resumo em risks.md: recursão no teste de `make check` (R-1), ambiente sem `.venv` (R-2), CI e Makefile tocando enforcement (R-3), ruff restrito ao produto (R-4), cópia do repositório no teste de AC-3 (R-5) e teste do tooling vermelho até o G0, como falha conhecida (R-6). O risco do download do Chromium para o e2e está na ADR-002 (Riscos).

## Out of scope
- Filtro, contador, estados vazio e de erro (F-CATALOGO-V1).
- Deploy, servidor de produção (gunicorn etc.), Docker.
- e2e obrigatório na CI.
- Tema escuro, internacionalização.

## NFRs
Herdados da Constitution §3. Suíte padrão hermética (sem rede; `make app-setup` e `make e2e-setup` são os únicos comandos que acessam a rede). Overrides: nenhum.

## NEEDS_CLARIFICATION
- ~~Q-2~~ (resolvida em 2026-10-28; lápide). A mantenedora autorizou revisar F-SDD-TOOLING-V1 AC-8 (v0.2.0): pending exige “Produto a definir”, complete proíbe, e os dois casos são testados. Consequência: enquanto PROD-001 estiver em `bootstrap: pending` com o texto da proposta, `make check` falha nesse teste até o G0 (ver Q-3). Texto original: (bloqueia `make check` verde): o teste do tooling `test_bootstrap_and_templates_are_product_independent` (F-SDD-TOOLING-V1 AC-8, `scripts/tests/test_hooks.py:132`) exige que PROD-001 contenha “Produto a definir” e que a Constitution contenha “a definir no bootstrap”. Desde a proposta de PROD-001 (2026-10-28), `make check` falha nesse teste. É um invariante do repositório-template, não do produto. Proposta: revisar F-SDD-TOOLING-V1 AC-8 para exigir isso só enquanto `bootstrap: pending` e checar apenas os `_TEMPLATE`. Isso mexe em enforcement e precisa de autorização explícita. Alternativa: manter a falha registrada como conhecida até decidir. Nunca silenciar o teste.
- ~~Q-3~~ (resolvida em 2026-10-28; lápide): a mantenedora escolheu a opção (a). `make check` fica vermelho em `test_bootstrap_and_templates_are_product_independent` até o G0, como falha conhecida, sem texto acrescentado ao PROD-001. A asserção da Constitution entrou na mesma revisão da AC-8 do tooling (v0.3.0), restrita à §2. Texto original: no intervalo entre a proposta e o G0, PROD-001 em `pending` sem “Produto a definir” deixa `make check` vermelho. Opções: (a) aceitar o vermelho conhecido até o G0, quando `bootstrap: complete` resolve; (b) acrescentar ao PROD-001 uma linha verdadeira como “Produto a definir: esta é uma proposta aguardando G0” e removê-la no G0. Também falta decidir: o mesmo teste exige que a Constitution contenha “a definir no bootstrap”, o que vai falhar quando a §2 for preenchida após o G2 (mesma família da Q-2, fora da autorização atual).
- ~~Q-1~~ (resolvida em 2026-10-28; lápide): a mantenedora aceitou Playwright + Chromium em `make e2e`, fora da CI nesta fase; AC-8 da F-CATALOGO-V1 mantida. Texto original: (muda o desenho dos testes de teclado): aceitar Playwright + Chromium (~150 MB, comando separado e fora da CI) para verificar teclado/foco e gerar capturas? Proposta: sim. Plano B: verificação manual roteirizada, registrada no design.md, sem AC-8 automatizada na F-CATALOGO-V1.
