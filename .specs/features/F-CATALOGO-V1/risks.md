---
id: RISK-F-CATALOGO-V1
kind: risks
title: Riscos — F-CATALOGO-V1
parent: F-CATALOGO-V1
version: 0.1.0
status: approved
last_updated: 2026-10-28
---

# Riscos (reais, avaliados; risco fechado ganha lápide, não é apagado)

| ID | Sev | Risco | Mitigação | Status |
|---|---|---|---|---|
| R-1 | ALTO | `\d`, `str.isdigit()` e `int()` em Python aceitam dígitos Unicode (`٢٠٢٤`, `２０２４`); a implementação “óbvia” violaria AC-5 sem que testes só com ASCII percebessem | `re.fullmatch(r"[0-9]{4}", ...)`; casos não ASCII no teste parametrizado; contraprova trocando por `\d{4}` numa cópia | aberto |
| R-2 | MÉDIO | `aplicado` vem do cliente e pode ser adulterado na URL (`aplicado=abc`, `aplicado=` com marcação) | Mesma validação de `ano`; inválido = todos (D-6); caso de teste dedicado | aberto |
| R-3 | MÉDIO | Recarregar a página tira o foco do campo; quem usa teclado precisaria voltar com Tab após cada filtro válido | Autofocus no erro (AC-7); depois de filtro válido, o foco no topo é aceito na V1 e registrado no design.md como limitação | aberto |
| R-4 | MÉDIO | Texto digitado devolvido ao campo (AC-5) abre espaço para injeção de HTML se o autoescape for desativado | Autoescape padrão do Jinja para `.html`; caso de teste com marcação; proibição de filtro `safe` no template | aberto |
| R-5 | MÉDIO | AC-8 roda fora de `make check` e da CI; uma regressão de teclado pode passar despercebida | `make e2e` obrigatório antes do fechamento e registrado em tasks.md; levar e2e à CI é pendência no postmortem | aberto |
| R-6 | BAIXO | Testes acoplados a texto exato quebram com ajuste de redação | Intencional: o texto é contrato (D-9, AC-4, AC-5); mudança de texto muda a spec primeiro | aceito |
