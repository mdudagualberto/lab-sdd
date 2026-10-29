---
id: PM-catalogo-bootstrap-2026-10-28
kind: postmortem
title: Bootstrap do catálogo — F-SETUP-V1 e F-CATALOGO-V1
parent: F-CATALOGO-V1
version: 1.0.0
status: draft
risk_tier: minimal
owners: [mdudagualberto]
related_adrs: [ADR-002]
last_updated: 2026-10-28
index: false
---

# PM — Bootstrap do catálogo (F-SETUP-V1 e F-CATALOGO-V1)
kind: **feature-close**

## §1. Objetivo
Do template sem produto até um catálogo local em Flask com filtro por ano, contador, lista vazia e erro de entrada. A base foram os critérios do guia pós-aula, com 12 decisões de comportamento registradas.
Gates G0, G2 e G1 aceitos pela mantenedora em 2026-10-28 (df98191). Implementação por AC, com teste vermelho antes do verde, em 6ac3964 e 0e41e52; correções da revisão independente em 49a4403.
Verificação final em 49a4403: `make check` verde e `make e2e` verde. A CI remota e o aceite final (`approved`) continuam pendentes.

## §2. Funcionou ✅
- **Teste antes do código em todas as ACs.** O vermelho registrado em tasks.md mostra o motivo de cada falha. Em duas ACs, a primeira falha foi de marcação (lista vazia) e não de comportamento. Nesses casos, acrescentei só a marcação e registrei um segundo vermelho, agora de comportamento (F-CATALOGO T-002).
- **O vermelho da AC-2 da F-SETUP mostrou o risco R-1 na prática.** `int("２０２４")` funciona em Python: com `ErroDados` vazio, os casos não ASCII passavam calados. Uma única regra ASCII (`ANO` em `catalogo/dados.py`) é usada pela carga e pelo filtro.
- **Contraprovas em cópias temporárias**, sempre com um controle que passa: fronteira DS-00, regex `\d{4}`, `autofocus`, regras do DS, AC-8 do tooling.
- **Revisor independente** (subagente `spec-reviewer`, somente leitura): encontrou 1 defeito de produto e 2 mutantes sobreviventes que a minha própria verificação não pegou. Também regenerou as 10 capturas numa cópia de 0e41e52 e elas saíram idênticas byte a byte.
- **Separação entre o `check` do template e o do produto** (`check-template` contra `check`). O job da CI em Python 3.9 continua validando o tooling, sem precisar do `.venv` do produto.

## §3. Deu errado ⚠️
### Bug 1 — Ano exibido sem zeros à esquerda
- **Sintoma:** um artigo com `"ano": "0999"` aparecia como `999`, e `0000` como `0`.
- **Root cause:** `Artigo.ano` é `int`, e o template mostrava o número sem formatar. Nem a spec nem os testes diziam como o ano é exibido.
- **Evidência:** `tests/catalogo/test_filtro_ano.py::test_ac1_ano_exibido_mantem_quatro_digitos` (2 failed antes da correção).
- **Fix:** `"%04d" | format(artigo.ano)` no template (49a4403).
- **Impacto:** só nos dados com ano abaixo de 1000; os dados de demonstração e a fixture não têm nenhum. A filtragem estava correta.
- **Detecção:** revisão independente, por sondagem HTTP numa cópia.

### Bug 2 — Testes que não derrubavam mutantes plausíveis
- **Sintoma:** dois mutantes passavam em todos os 56 testes: `{{ artigo.titulo | safe }}` e `ANO` com `$` + `match` no lugar de `fullmatch`. Com o segundo, `"2024\n"` era aceito nos dados.
- **Root cause:**
  - O helper `Pagina.titulos` usa `get_text`, que devolve o mesmo texto com ou sem escape.
  - Os casos inválidos de AC-2 não tinham espaço nem quebra de linha. No filtro, o `strip()` esconde a diferença; nos dados, não há strip.
- **Evidência:** `tests/catalogo/test_entrada_invalida.py::test_d12_titulo_e_autores_dos_dados_aparecem_escapados` e os casos novos em `tests/test_dados.py`. Os dois mutantes agora falham.
- **Fix:** 49a4403.
- **Impacto:** nenhum defeito em produção; era uma lacuna de verificação. R-4 prometia algo que nenhum teste cobrava.
- **Detecção:** revisão independente, por mutação.

### Bug 3 — Regra de DS sem enforcement e controle que podia ser pulado
- **Sintoma:**
  - A R1 do DS-07 exigia o prefixo `Erro`, mas `class DadosError` passava no ruff (N818 desligado).
  - Exportar `CATALOGO_TESTE_INTERNO=1` pulava a AC-3 da F-SETUP em silêncio, e o teste fixava `VENV=RAIZ/.venv`.
- **Root cause:**
  - Desliguei o N818 sem pôr outro enforcement no lugar.
  - A proteção contra recursão usava uma variável que qualquer pessoa pode exportar.
- **Evidência:** `tests/test_convencoes.py::test_excecoes_do_dominio_usam_prefixo_erro`. Em `tests/test_comandos.py`, um marcador `.catalogo-teste-interno` que só existe na cópia, e `VENV=sys.prefix`.
- **Fix:** 49a4403.
- **Impacto:** baixo.
- **Detecção:** revisão independente.

### Bug 4 — Invariante do template quebrava o bootstrap
- **Sintoma:** `make check` ficou vermelho logo depois da proposta de PROD-001. O teste exigia "Produto a definir" sempre.
- **Root cause:** a AC-8 da F-SDD-TOOLING-V1 descrevia o estado do repositório-template, não o estado do bootstrap.
- **Evidência:** `.specs/features/F-SDD-TOOLING-V1/spec.md` v0.3.0; `scripts/tests/test_hooks.py::test_bootstrap_placeholder_follows_bootstrap_state`.
- **Fix:** df98191, com autorização da mantenedora. A regra depende de `bootstrap` em PROD-001 e na §2 da Constitution, e os dois casos são testados.
- **Impacto:** o check ficou vermelho, como falha conhecida aceita, até o G0.
- **Detecção:** o primeiro `make check` depois da proposta.
- **Falha minha no caminho:**
  - A primeira contraprova desse teste copiou só `scripts/`, então dava *error* até sem mutação. Só a considerei válida depois de refazer com a árvore inteira e o controle passando.
  - O mutante "aceita estado inválido" passou na primeira versão do teste e exigiu reforçar a asserção.

## §4. Métricas
Medido em 49a4403 com os comandos indicados. A baseline é db751f6.

| Métrica | Baseline | Medido | Delta |
|---|---|---|---|
| Testes do tooling (`make test`) | 24 | 25 | +1 (AC-8 do bootstrap) |
| Testes do produto no `make check` (`app-test`) | 0 | 64 passed | +64 |
| Testes e2e (`make e2e`) | 0 | 3 passed (+10 capturas, só com `EVIDENCIA=1`) | +3 |
| ACs com `@test:` apontando arquivo existente | 0 | 12/12 (F-SETUP 4, F-CATALOGO 8) | +12 |
| Capturas por estado inspecionadas e aprovadas | 0 | 10/10 (agente + mantenedora) | +10 |
| Mutantes da revisão sobreviventes | — | 0 de 3 depois de 49a4403 (3 antes) | −3 |
| Arquivos alterados (db751f6..HEAD, antes deste PM) | — | 62 (+1983/−39) | — |

## §5. Lições
1. Um teste de AC que lê só o texto visível (`get_text`) não prova escape nem formato. Para saída que pode carregar marcação, o teste confere o HTML bruto. → fix concreto: `tests/catalogo/test_entrada_invalida.py::test_d12_...`. Se o padrão se repetir numa segunda tela, ele vira regra de DS-06.
2. Desligar uma regra de lint exige pôr outro enforcement no lugar, no mesmo commit. → fix concreto: ratchet em `tests/test_convencoes.py` e DS-07 1.1.0.
3. Proteção contra recursão em teste de comando não pode depender de algo que o ambiente externo define (variável de ambiente). → fix concreto: marcador criado só na cópia (DS-06 1.0.1, R5).
4. Contraprova sem um controle que passa não prova nada: uma cópia incompleta faz o teste falhar pelo motivo errado. → fix concreto: todas as contraprovas desta entrega rodaram com controle; as que não tinham foram refeitas.
5. A revisão independente encontrou defeitos que a autoverificação deixou passar. → processo: `spec-reviewer` antes do aceite final (CLAUDE.md, passo 5), com instrução de atacar por mutação.

- **Spec gap identificado:**
  - (a) A F-CATALOGO-V1 D-4 e a AC-1 não dizem como o ano é exibido. O código agora mostra sempre quatro dígitos, coberto pelo teste novo da AC-1, mas a frase não está na spec. → revisão de spec pendente (§6).
  - (b) A AC-8 da F-SDD-TOOLING-V1 tratava o repositório como template permanente → corrigida na v0.3.0 (df98191).
  - (c) A spec não define o caso do parâmetro `ano` repetido na URL (`args.get` usa o primeiro valor). O texto da D-3 não menciona espaços Unicode que `strip()` também remove. → itens informativos (§6).
- **Convenção descoberta:** nenhuma além da semente. A classe `Pagina` com um oráculo independente aparece numa única tela, e o prefixo `Erro` já está no DS-07.

Não atualizei `docs/learned-practices.md`. A única prática reutilizável fora deste produto é a AC-8 depender do estado do bootstrap, e ela pertence ao template de origem. Fica como proposta para o upstream (§6), sem alterar o guia local do método.

## §6. Pendências (declare `nenhuma` explicitamente se for o caso)
| Pendência | Tipo (prevent/mitigate/process) | Owner | Prazo | Tracking | Status |
|---|---|---|---|---|---|
| Resultado real da CI (jobs `check` e `product`), que depende de push | process | mdudagualberto | antes do aceite final | F-SETUP-V1 T-007 | aberto |
| Revisão humana do código e aceite final (`approved`) das specs | process | mdudagualberto | antes da entrega ao grupo | F-SETUP-V1 / F-CATALOGO-V1 status_history | aberto |
| Escrever na spec que o ano é exibido com quatro dígitos (D-4/AC-1), numa revisão 0.1.2 | prevent | mdudagualberto (decide) | próxima rodada (intervalo de anos) | este PM §5 (a); F-CATALOGO-V1 v0.1.2 | feito em 2026-10-28 |
| Verificação com leitor de tela real | mitigate | mdudagualberto | sem prazo; fora da V1 | F-CATALOGO-V1 T-009 | deferred |
| Levar `make e2e` para a CI | prevent | mdudagualberto | quando o custo do Chromium na CI for aceito | F-CATALOGO-V1 risks R-5 | aberto |
| Decidir o caso do `ano` repetido na URL e o texto da D-3 | process | mdudagualberto | opcional | este PM §5 (c) | aberto |
| Propor ao template de origem a AC-8 que depende do bootstrap | process | mdudagualberto | opcional | F-SDD-TOOLING-V1 v0.3.0 | aberto |
| Rodar o tooling em Python 3.9 (só há 3.12 localmente) | mitigate | CI (job `check`) | no primeiro push | ci.yml | aberto |

## §7. Evidências (paths reproduzíveis — confirme que existem antes de escrever)
- Commits: df98191 (gates), 6ac3964 (F-SETUP-V1), 0e41e52 (F-CATALOGO-V1), 49a4403 (correções da revisão).
- `.specs/features/F-SETUP-V1/tasks.md` e `.specs/features/F-CATALOGO-V1/tasks.md`: vermelho, verde e contraprova por task.
- `.specs/features/F-CATALOGO-V1/design.md`: conferência visual e contraste.
- `docs/images/F-CATALOGO-V1-*.png`: 10 capturas.
- `tests/e2e/test_teclado.py` (AC-8) e `tests/test_comandos.py` (AC-3 da F-SETUP).
- `.specs/features/F-SDD-TOOLING-V1/spec.md` (AC-8 v0.3.0) e `scripts/tests/test_hooks.py`.
- Revisão independente: relatório do subagente `spec-reviewer` nesta sessão, veredito APROVAR COM RESSALVAS. Não ficou persistido em arquivo; os achados estão resumidos em §3 e nas tasks T-009 (F-SETUP) e T-010 (F-CATALOGO).
- Não executado: CI remota, Python 3.9, Firefox/Safari, teclado físico, leitor de tela.
