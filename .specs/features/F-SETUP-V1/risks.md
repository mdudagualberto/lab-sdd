---
id: RISK-F-SETUP-V1
kind: risks
title: Riscos — F-SETUP-V1
parent: F-SETUP-V1
version: 0.1.0
status: in_review
last_updated: 2026-10-28
---

# Riscos (reais, avaliados; risco fechado ganha lápide, não é apagado)

| ID | Sev | Risco | Mitigação | Status |
|---|---|---|---|---|
| R-1 | MÉDIO | `tests/test_comandos.py` roda `make check`, que roda pytest, que roda `test_comandos` de novo (recursão) ou fica lento | Variável `CATALOGO_TESTE_INTERNO=1` pula o teste na execução interna; a contraprova confirma que a falha proposital ainda derruba o comando | aberto |
| R-2 | MÉDIO | `make check` passa a exigir `.venv`; num clone novo, sem `make app-setup`, o erro fica obscuro | Alvos do produto checam `$(VENV)/bin/python` e falham com uma mensagem que manda rodar `make app-setup`; falha nunca vira “pulado” | aberto |
| R-3 | MÉDIO | Mudar `ci.yml` e `Makefile` mexe no enforcement do template (AGENTS Regra 9) | Manter os passos originais intactos e só acrescentar os do produto; `make test` do tooling continua no `check`; revisão somente leitura do diff | aberto |
| R-4 | BAIXO | O ruff varrendo `scripts/` (tooling) acusaria código que não é do produto | Configuração restrita a `catalogo` e `tests` | aberto |
| R-6 | ALTO | O teste do tooling que exige template intacto falha depois do bootstrap; um `make check` vermelho “conhecido” vira ruído e esconde falhas novas | Q-2 e Q-3 resolvidas (2026-10-28): o teste segue o estado do bootstrap em PROD-001 e na §2 da Constitution (F-SDD-TOOLING-V1 v0.3.0). Até o G0 o vermelho é falha conhecida aceita pela mantenedora (opção a); todo resultado de verificação cita o teste pelo nome, e qualquer outra falha conta como nova | ~~aceito até o G0~~ fechado em 2026-10-28 (lápide): G0 registrado em df98191, `bootstrap: complete`, `make check` verde |
| R-5 | BAIXO | A cópia do repositório em AC-3 usa o `.git` real e poderia alterar estado | Cópia com `shutil.copytree` para `tmp_path`; nenhum comando Git que escreva roda na cópia; o original não é tocado | aberto |
