---
id: PLAN-F-SETUP-V1
kind: plan
title: Plano — F-SETUP-V1
parent: F-SETUP-V1
version: 0.1.0
status: approved
last_updated: 2026-10-28
---

# Plano

## Estratégia
Começar pelo teste de cada AC, ver falhar pelo motivo esperado (módulo ou comportamento ausente) e implementar o mínimo. O esqueleto existe para provar a stack e a cadeia de verificação. Só depois que o código existir escrever os DS-00/06/07, que descrevem esse código, cada um com seu enforcement no mesmo commit.

Pré-condições: G2 aceito para a ADR-002 (com a Constitution §2 preenchida no mesmo commit), G1 aceito para esta spec → `status: in_review` → `echo F-SETUP-V1 > .sdd/active-spec`.

## Arquivos tocados
| Caminho | Conteúdo |
|---|---|
| `requirements.txt`, `requirements-dev.txt` | Pins exatos (Flask 3.1.x; pytest 8.x, beautifulsoup4, playwright, ruff) |
| `pyproject.toml` | Metadados mínimos, config do ruff (só `catalogo` e `tests`) e do pytest (`testpaths`, `--strict-markers`) |
| `catalogo/__init__.py`, `catalogo/__main__.py` | Pacote; `python -m catalogo` |
| `catalogo/dados.py` | `Artigo`, `ErroDados`, `carregar_artigos` |
| `catalogo/web.py` | `create_app(caminho_dados=None)`, rota `GET /` |
| `catalogo/templates/catalogo.html`, `catalogo/static/estilo.css` | Página mínima (h1 + lista) |
| `data/artigos.json` | ~10 artigos fictícios, anos 2021–2025, com 2024 tendo 3 itens |
| `tests/conftest.py`, `tests/fixtures/artigos.json` | Fixture `app`/`client` com dados de teste próprios |
| `tests/test_smoke.py`, `tests/test_dados.py`, `tests/test_comandos.py`, `tests/test_arquitetura.py` | AC-1..AC-4 |
| `Makefile` | Alvos `app-setup`, `app-lint`, `app-test`, `e2e-setup`, `e2e`, `run`; `check` passa a incluir `app-lint` e `app-test`; variável `VENV ?= .venv` |
| `.github/workflows/ci.yml` | Python 3.12, `make app-setup`, `make check` |
| `.specs/design-system/DS-00-arquitetura.md`, `DS-06-testes.md`, `DS-07-nomes.md` | Semente com enforcement |
| `.specs/constitution/constitution.md` | §2 preenchida (bump 1.2.0) **após G2** |
| `CLAUDE.md` / `README.md` | Linha com os comandos do produto |

## Passos (ordem; marque ✅ ao concluir)
Passos 1–6 e 8 ✅ em 2026-10-28 (evidência em tasks.md). Passo 7 ✅: CI verde em 227ea63 (https://github.com/mdudagualberto/lab-sdd/actions/runs/40811044546). Passo 9: em andamento. Desvio do plano: `check-template` preserva o check original e é o que o job do template na CI roda (Python 3.9), porque o `check` completo exige o `.venv` do produto.
1. `requirements*.txt`, `pyproject.toml`, alvo `app-setup`; rodar `make app-setup` (rede, PyPI) e registrar as versões instaladas.
2. AC-1: `tests/test_smoke.py` vermelho (ImportError de `catalogo.web`) → `create_app` + template → verde.
3. AC-2: `tests/test_dados.py` com casos válido (`"2024"` vira `2024`), JSON malformado, campo ausente, autores vazio, ano `"24"`, `"20245"`, `"２０２４"` (dígitos de largura total) e inteiro JSON `2024` → vermelho → `dados.py` → verde.
4. AC-4: `tests/test_arquitetura.py` (varre `catalogo/*.py` com `ast`, procura imports de `flask`/`jinja2`) → contraprova: inserir `import flask` em `dados.py` numa cópia e confirmar a falha com a mensagem citando DS-00.
5. Makefile: `app-lint`, `app-test`, `run`, `e2e-setup`, `e2e`; `check` estendido. Rodar `make check`.
6. AC-3: `tests/test_comandos.py` copia o repositório (incluindo `.git`, sem `.venv`) para `tmp_path`, roda `make check VENV=$REPO/.venv` (caminho absoluto do `.venv` original) com `CATALOGO_TESTE_INTERNO=1` (que pula o próprio `test_comandos` na execução interna, evitando recursão) e espera código 0. Depois grava `tests/test_falha_proposital.py` (`assert False`) na cópia e espera código ≠ 0.
7. CI: atualizar `ci.yml`; conferir a sintaxe; o resultado real da CI só existe depois de push (não autorizado nesta etapa → pendente).
8. `/ds-new` para DS-00, DS-06 e DS-07, com exemplos `path:linha` reais e linhas de enforcement (`test_arquitetura.py`, config do ruff, `testpaths`/marcadores do pytest).
9. `make sdd`, `make check`; revisão `spec-reviewer` somente leitura; postmortem proporcional; limpar `.sdd/active-spec`.

## Diferidos
- e2e na CI (depende de Q-1 e do custo do navegador na CI).
- Servidor de produção, empacotamento e Docker: fora do produto.

## Verificação
- `make app-test` (pytest do produto) · `make app-lint` (ruff) · `make check` (template + produto) · `make sdd` após editar specs.
- Build: não se aplica (Python); o teste de fumaça (AC-1) prova a inicialização.
- Contraprovas: AC-3 (teste falhando derruba `make check`) e AC-4 (import proibido derruba o teste).

## Contratos e compatibilidade
Fonte única do formato de dados: `catalogo/dados.py` (`Artigo` e as validações de `carregar_artigos`). `data/artigos.json` e `tests/fixtures/artigos.json` seguem esse formato, e a F-CATALOGO-V1 consome `Artigo`. Não há versões publicadas nem compatibilidade a manter.

## Design e evidências
Sem interface de usuário própria: a página do esqueleto é um marcador de fumaça. O contrato visual está em DESIGN-F-CATALOGO-V1 (ver design.md desta feature, `applicable: false`).

## Recursos compartilhados
Sem paralelismo planejado. A porta 5000 é usada só por `make run`; os testes usam o cliente do Flask (sem porta) e o e2e escolhe uma porta livre.
