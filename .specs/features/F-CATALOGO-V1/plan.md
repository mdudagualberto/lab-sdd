---
id: PLAN-F-CATALOGO-V1
kind: plan
title: Plano — F-CATALOGO-V1
parent: F-CATALOGO-V1
version: 0.1.0
status: in_review
last_updated: 2026-10-28
---

# Plano

## Estratégia
Implementar por AC sobre o esqueleto da F-SETUP-V1: para cada AC, escrever o teste, registrar a falha real (comando e saída resumida em tasks.md), implementar o mínimo e registrar o verde. A regra de filtro vive em `catalogo/filtro.py` (puro). Os testes de AC passam pela página renderizada (cliente do Flask + beautifulsoup4), porque o efeito observável é o que a pessoa vê. Testes unitários de `filtro.py` podem existir como apoio, mas não substituem os de AC.

Pré-condições: F-SETUP-V1 concluída, ADR-002 aceita (G2), G1 desta spec → `status: in_review` → `echo F-CATALOGO-V1 > .sdd/active-spec`.

## Arquivos tocados
| Caminho | Conteúdo |
|---|---|
| `catalogo/filtro.py` | `interpretar_entrada(texto) -> Entrada` (vazia / ano / inválida), `filtrar(artigos, ano_ou_none)` |
| `catalogo/web.py` | Rota `GET /` lê `ano` e `aplicado`, decide filtro efetivo e erro, renderiza |
| `catalogo/templates/catalogo.html` | Formulário, ajuda, erro, contador, lista, estado vazio |
| `catalogo/static/estilo.css` | Layout de uma coluna, foco visível, cor de erro com contraste AA |
| `tests/fixtures/artigos.json` | 8 artigos: 2024 ×3 (não consecutivos no arquivo), 2023 ×2, 2022, 2021, 2025; nenhum de 1999/0000 |
| `tests/catalogo/conftest.py` | Helpers: `itens(html)`, `contador(html)`, `erro(html)` com beautifulsoup4 |
| `tests/catalogo/test_filtro_ano.py` | AC-1, AC-3 |
| `tests/catalogo/test_contador.py` | AC-2 |
| `tests/catalogo/test_lista_vazia.py` | AC-4 |
| `tests/catalogo/test_entrada_invalida.py` | AC-5 (parametrizado: `abc`, `202`, `20245`, `２０２４`, `٢٠٢٤`, `+2024`, `20 24`, `2024.0`, marcação HTML), AC-6, D-6 (`aplicado` adulterado) |
| `tests/catalogo/test_acessibilidade.py` | AC-7 |
| `tests/e2e/conftest.py`, `tests/e2e/test_teclado.py` | Servidor em thread numa porta livre com a fixture; AC-8; capturas com `EVIDENCIA=1` |
| `docs/images/F-CATALOGO-V1-*.png` | Evidências por estado e variante (design.md) |

## Passos (ordem; marque ✅ ao concluir)
1. Fixture e helpers de leitura do HTML.
2. AC-1 + AC-3 (filtro e limpar) → vermelho → `filtro.py` + rota → verde.
3. AC-2 (contador nos quatro estados) → vermelho → template → verde.
4. AC-4 (vazio) → vermelho → template → verde.
5. AC-5 + AC-6 (erro, preservação via `aplicado`, remoção do erro) → vermelho → `interpretar_entrada` com `re.fullmatch(r"[0-9]{4}", ...)` → verde. Contraprova: trocar por `\d{4}` numa cópia e confirmar que os casos `２０２４`/`٢٠٢٤` falham.
6. AC-7 (marcação acessível) → vermelho → template → verde.
7. AC-8 (`make e2e`) → vermelho → ajustes de template (autofocus, ordem) → verde.
8. Capturas por estado e variante (`EVIDENCIA=1 make e2e`); inspecionar cada imagem e preencher “Conferência visual” no design.md.
9. `make sdd`, `make check`, `make e2e`; revisão `spec-reviewer` somente leitura; `/postmortem`; limpar `.sdd/active-spec`.

## Diferidos
- Intervalo de anos: próxima revisão do contrato desta feature.
- Teste com leitor de tela real (Orca/NVDA): pendência registrada no design.md, dona: mantenedora.

## Verificação
- `make app-test` (AC-1..AC-7) · `make e2e` (AC-8 + capturas) · `make app-lint` · `make check` · `make sdd` após editar specs.
- Build: não se aplica (ADR-002).
- Contraprova obrigatória: regra de quatro dígitos ASCII (passo 5).

## Contratos e compatibilidade
Contrato de entrada: query string `ano` (texto livre) e `aplicado` (último ano válido). Única fonte da regra: `catalogo/filtro.py`. `Artigo` vem de `catalogo/dados.py` (F-SETUP-V1). Não há API pública, versões publicadas nem consumidores externos.

## Design e evidências
design.md desta feature: estados inicial, filtrado, vazio, erro a partir do inicial, erro a partir do filtrado, recuperação; variantes desktop (1280×800) e celular (375×800). Evidências em `docs/images/`.

## Recursos compartilhados
Sem paralelismo. O e2e usa porta livre escolhida pelo sistema (porta 0), sem conflito com `make run`.
