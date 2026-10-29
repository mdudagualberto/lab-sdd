---
id: DESIGN-F-CATALOGO-V1
kind: design
title: Design — F-CATALOGO-V1
parent: F-CATALOGO-V1
version: 0.2.0
status: in_review
applicable: true
last_updated: 2026-10-28
---

# Design — estado por estado

Contrato de implementação visual; não substitui a spec. Se não houver UI, use `applicable: false` e justifique em Referências; mantenha as demais seções com “não se aplica”.

## Referências
- Spec e versão: `.specs/features/F-CATALOGO-V1/spec.md` v0.1.2.
- Referência visual: wireframe W-1 abaixo, versionado neste arquivo (v0.1.0). Não há Figma; o wireframe decide a disposição e o CSS mínimo decide o resto.
- Superfícies e variantes: navegador desktop (1280×800) e largura de celular (375×800); tema claro; pt-BR. Tema escuro e outros idiomas: não aplicáveis na V1 (PROD-001 P-3).
- Componentes existentes e implementação: `catalogo/templates/catalogo.html` (formulário, ajuda, erro, contador, lista, vazio) e `catalogo/static/estilo.css`.
- Tokens e fonte canônica: sem biblioteca de tokens. Cores e espaçamentos ficam em variáveis CSS em `catalogo/static/estilo.css` (fonte única; sem geração).
- Responsável pela revisão: mantenedora (mdudagualberto).

Spec decide comportamento, fluxo e texto; referência visual decide aparência. Divergência não autoriza inventar: registre abaixo e resolva com o responsável antes da implementação afetada.

### W-1 — wireframe (desktop; no celular, os mesmos blocos empilham em uma coluna)
```
┌──────────────────────────────────────────────────────┐
│ Catálogo de artigos                         (h1)     │
│                                                      │
│ Ano de publicação                          (label)   │
│ ┌───────────────┐ ┌─────────┐                        │
│ │ 2024          │ │ Filtrar │                        │
│ └───────────────┘ └─────────┘                        │
│ Quatro dígitos, por exemplo 2024. Deixe vazio        │
│ para ver todos.                            (ajuda)   │
│ ! Informe um ano com quatro dígitos   (erro; só E-4/E-5)│
│                                                      │
│ Artigos exibidos: 3                        (contador)│
│ ──────────────────────────────────────────────────── │
│ Título do artigo A                         (negrito) │
│ Autora Fictícia 1, Autor Fictício 2 · 2024           │
│ ──────────────────────────────────────────────────── │
│ Título do artigo B ...                               │
│                                                      │
│ (E-3: no lugar da lista) Nenhum artigo encontrado    │
└──────────────────────────────────────────────────────┘
```

## Estado por estado
Uma linha por estado e variante relevante; incluir inicial, carregamento, sucesso, vazio, erro, sem permissão, offline e recuperação quando aplicáveis. Justificar variantes não aplicáveis.

| Estado / AC | Superfície / variante | Referência visual | Componentes / tokens | Texto e ação | Teclado / foco / acessibilidade |
|---|---|---|---|---|---|
| E-1 Inicial (D-1) / AC-2 | desktop, celular | W-1 sem erro | form, ul, p#contador | Campo vazio; todos os artigos; “Artigos exibidos: 8” (fixture) | Sem autofocus; Tab: campo → Filtrar (AC-8); ajuda ligada por aria-describedby |
| E-2 Filtrado / AC-1, AC-2 | desktop, celular | W-1 sem erro | idem | Campo com “2024”; só os 3 de 2024; “Artigos exibidos: 3” | Enter no campo aplica (AC-8); depois de recarregar, foco volta ao topo (limitação R-3) |
| E-3 Vazio / AC-4, AC-2 | desktop, celular | W-1, bloco “Nenhum artigo encontrado” no lugar da lista | p no lugar da ul | “1999”; “Nenhum artigo encontrado”; “Artigos exibidos: 0” | Mensagem é texto comum (não é erro, sem role="alert") |
| E-4 Erro a partir do inicial / AC-5, AC-7 | desktop, celular | W-1 com linha de erro | p#erro-ano, campo inválido | Campo mantém “abc”; “Informe um ano com quatro dígitos”; lista completa; “Artigos exibidos: 8” | Campo com autofocus, aria-invalid="true" e aria-describedby com erro e ajuda; erro com role="alert"; cor + ícone “!” (não só cor) |
| E-5 Erro a partir do filtrado / AC-5, AC-2 | desktop | W-1 com linha de erro | idem | `aplicado=2024`, campo “20245”; erro; continuam os 3 de 2024; “Artigos exibidos: 3” | Igual a E-4 |
| E-6 Recuperação / AC-6, AC-3 | desktop | W-1 sem erro | idem | De E-4, aplicar “2023” (ou vazio) → erro some; resultado correspondente | Sem aria-invalid; sem autofocus |
| Carregamento | — | — | — | Não se aplica: renderização síncrona no servidor com dados locais | — |
| Sem permissão / offline | — | — | — | Não se aplica: sem login nem rede (PROD-001 §8) | — |

## Diferenças conhecidas
| Diferença spec × referência | Decisão / fonte vencedora | Responsável | Status |
|---|---|---|---|
| Nenhuma registrada (o wireframe foi escrito a partir da spec v0.1.0) | — | mantenedora | — |

## Lacunas
- L-1: indicador de “filtro atual” (por exemplo “Filtrando por 2024”) não existe. Em E-5, o campo mostra “20245” enquanto a lista mostra 2024, o que pode confundir. Decisão proposta: fora da V1, porque o erro já explica a situação. Reavaliar na revisão de intervalo de anos.
- L-2: anúncio do resultado por leitor de tela após filtro válido. Com recarga completa, não há região viva útil. Fora da V1; T-009 deferred.
- ~~L-3~~ (resolvida em 2026-10-28; lápide): contraste calculado pela fórmula WCAG a partir das variáveis de `catalogo/static/estilo.css`: texto 15,80:1; texto suave 6,39:1; erro 6,54:1; botão 6,67:1; borda do campo 3,04:1 e foco 6,67:1 (não texto, meta 3:1). Todos dentro da meta AA. Texto original: contraste exato das cores não tem referência externa. Será medido nas capturas (meta WCAG AA 4,5:1 para texto) e registrado abaixo.

## Conferência visual
Build verde não prova aparência nem acessibilidade. Abra e inspecione cada captura; depois exercite interação, foco e tecnologia assistiva conforme as ACs. Separe “inspecionado em imagem” de “testado interativamente”.

| Estado / variante | Build ou commit | Evidência persistente | Referência comparada | Resultado / revisor / data |
|---|---|---|---|---|
| E-1 desktop | 0e41e52 | docs/images/F-CATALOGO-V1-inicial-desktop.png | W-1 | inspecionado em imagem: 8 itens, contador 8, sem erro; confere com W-1; agente, 2026-10-28; aprovado pela mantenedora em 2026-10-28 |
| E-1 celular | 0e41e52 | docs/images/F-CATALOGO-V1-inicial-celular.png | W-1 | inspecionado em imagem: uma coluna, campo e botão na mesma linha, ajuda quebra em 2 linhas; confere; agente, 2026-10-28; aprovado pela mantenedora em 2026-10-28 |
| E-2 desktop | 0e41e52 | docs/images/F-CATALOGO-V1-filtrado-desktop.png | W-1 | inspecionado em imagem: campo “2024”, 3 itens de 2024, contador 3; confere; agente, 2026-10-28; aprovado pela mantenedora em 2026-10-28 |
| E-2 celular | 0e41e52 | docs/images/F-CATALOGO-V1-filtrado-celular.png | W-1 | inspecionado em imagem: idem em 375 px; confere; agente, 2026-10-28; aprovado pela mantenedora em 2026-10-28 |
| E-3 desktop | 0e41e52 | docs/images/F-CATALOGO-V1-vazio-desktop.png | W-1 | inspecionado em imagem: “Nenhum artigo encontrado” em caixa tracejada, contador 0, sem lista; confere; agente, 2026-10-28; aprovado pela mantenedora em 2026-10-28 |
| E-3 celular | 0e41e52 | docs/images/F-CATALOGO-V1-vazio-celular.png | W-1 | inspecionado em imagem: idem em 375 px; confere; agente, 2026-10-28; aprovado pela mantenedora em 2026-10-28 |
| E-4 desktop | 0e41e52 | docs/images/F-CATALOGO-V1-erro-desktop.png | W-1 | inspecionado em imagem: “abc” mantido, borda de erro, anel de foco, “! Informe um ano com quatro dígitos”, 8 itens; confere; agente, 2026-10-28; aprovado pela mantenedora em 2026-10-28 |
| E-4 celular | 0e41e52 | docs/images/F-CATALOGO-V1-erro-celular.png | W-1 | inspecionado em imagem: idem em 375 px; confere; agente, 2026-10-28; aprovado pela mantenedora em 2026-10-28 |
| E-5 desktop | 0e41e52 | docs/images/F-CATALOGO-V1-erro-filtrado-desktop.png | W-1 | inspecionado em imagem: “20245”, erro, continuam os 3 de 2024, contador 3; confere; agente, 2026-10-28; aprovado pela mantenedora em 2026-10-28 |
| E-6 desktop | 0e41e52 | docs/images/F-CATALOGO-V1-recuperacao-desktop.png | W-1 | inspecionado em imagem: de “abc” para “2023” com Enter; erro some, 2 itens, contador 2; confere; agente, 2026-10-28; aprovado pela mantenedora em 2026-10-28 |
| Teclado (AC-8) | mesmo build | saída de `make e2e` registrada em tasks.md T-007 | — | testado interativamente no Chromium headless (Playwright): Tab campo → Filtrar, Enter aplica, foco no campo após erro; 3 passed; contraprova sem autofocus falha. Não testado em Firefox/Safari nem com teclado físico |
| Leitor de tela | — | — | — | não verificado na V1 (T-009) |

Não use caminhos temporários como única evidência. Não inclua dados pessoais nas capturas. A task fecha com evidência e revisão registrada, ou fica explicitamente pendente.
