---
id: PROD-001
kind: product_spec
title: Catálogo local de artigos do grupo de estudos
parent: CONST-001
version: 0.1.1
status: in_review
bootstrap: complete
risk_tier: minimal
owners: [mdudagualberto]
last_updated: 2026-10-28
spec_hash: pending
status_history:
  - { version: 0.0.1, status: draft, date: 2026-09-05, note: "esqueleto; preenchido no Playbook Bootstrap a partir do case" }
  - { version: 0.1.0, status: draft, date: 2026-10-28, note: "proposta de bootstrap a partir do pedido da mantenedora e da seção 4 do guia pós-aula; aguarda G0 (bootstrap segue pending até o aceite)" }
  - { version: 0.1.1, status: in_review, date: 2026-10-28, note: "G0 sobre a versão 0.1.0: aceite da mantenedora em 2026-10-28 nesta conversa ("Revisei e aceito o produto, a stack e os contratos nestas versões"); não é aprovação final da entrega; bootstrap: complete; §5 atualizada para ADR-002 aceita" }
---

# PROD-001 — Catálogo local de artigos do grupo de estudos

## 1. Visão
Uma página local, executada na máquina de quem estuda, que lista os artigos do grupo de estudos e permite filtrar por ano de publicação. É também um projeto de aprendizado: cada comportamento da tela precisa ser rastreável de requisito a teste, implementação e evidência visual.

## 2. Públicos e jobs-to-be-done
| Público | Job-to-be-done |
|---|---|
| Membro do grupo de estudos | Ver rapidamente quais artigos do grupo são de um ano e quantos são. |
| Mantenedora (aprendiz de SDD) | Demonstrar o vínculo entre AC, teste que falha antes, implementação e evidência registrada em design.md. |
| Revisor(a) em dupla | Conferir, a partir do repositório, qual AC cobre cada estado da tela e qual teste falharia se a regra estivesse errada. |

## 3. Pilares
1. **Local e fictício.** Dados de exemplo inventados, versionados no repositório; sem rede, conta ou banco remoto.
2. **Pequeno e verificável.** Cada comportamento tem AC de uma linha e teste automatizado; estados visuais têm evidência persistente.
3. **Acessível pelo teclado.** O filtro funciona sem mouse e o erro é anunciado de forma programática.

## 4. Princípios de design
- Spec decide comportamento e texto; o wireframe versionado no design.md decide disposição; divergência é registrada.
- Mensagens em português do Brasil, curtas e literais (os testes comparam o texto exato).
- Erro de entrada nunca apaga o resultado que a pessoa já tinha na tela.
- HTML semântico nativo antes de comportamento customizado (formulário, rótulo e botão reais).

## 5. Arquitetura (visão)
Decidida em ADR-002 (accepted, G2 em 2026-10-28): aplicação Python local com Flask + Jinja, renderizada no servidor, lendo um arquivo JSON local somente leitura. Regra de filtro em módulo puro, sem dependência de Flask; camada web fina. Testes com pytest (cliente de teste do Flask) e verificação de teclado e capturas em navegador real com Playwright, num comando separado.

## 6. Métricas norte (instrumentadas vs aspiracionais)
| Métrica | Tipo | Como se mede |
|---|---|---|
| ACs com `@test:` existente e passando | Instrumentada | `make check` + resultado de pytest do produto registrado em tasks.md |
| Estados do design.md com captura persistente inspecionada | Instrumentada (manual) | Tabela “Conferência visual” do design.md |
| Tempo para alguém do grupo encontrar os artigos de um ano | Aspiracional | Não instrumentada nesta fase |

## 7. Roadmap (features F-*)
| Ordem | Feature | Escopo |
|---|---|---|
| 1 | F-SETUP-V1 | Esqueleto Python/Flask, carga validada dos dados fictícios, primeiro teste, lint, comandos do produto, CI e semente DS-00/06/07 |
| 2 | F-CATALOGO-V1 | Lista, filtro por ano, contador, lista vazia e erro de entrada |
| futuro | F-CATALOGO-V1 (revisão) | Intervalo de anos (seção 9 do guia); provavelmente revisão de contrato da mesma feature, sem nova ADR |

## 8. Não-objetivos
- Login, contas ou permissões.
- Qualquer chamada de rede ou API externa; banco remoto.
- Deploy ou hospedagem; o servidor escuta só em 127.0.0.1.
- Exportação BibTeX.
- Edição, cadastro ou exclusão de artigos pela interface (o conjunto de dados é editado no arquivo).
- Dados reais ou pessoais; os artigos e autores são fictícios.

## 9. NEEDS_CLARIFICATION
- nenhum bloqueante para G0. Premissas registradas abaixo; se alguma estiver errada, o desenho muda.

### 9.1 Premissas
- P-1. Uso individual e local; não há requisito de várias pessoas acessarem o mesmo servidor.
- P-2. Uma dezena de artigos fictícios basta; não há requisito de desempenho ou paginação.
- P-3. Interface só em pt-BR, tema claro; desktop e largura de celular são as variantes conferidas.
- P-4. A mantenedora prefere Python para o produto (instrução explícita de 2026-10-28).
