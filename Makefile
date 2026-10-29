.PHONY: help setup doctor sdd lint test check check-template
help:
	@printf '%s\n' 'setup: instala hooks e gera índice' 'doctor: verifica ambiente sem alterar' 'sdd: atualiza índice + lint + drift' 'check: checks do template + lint e testes do produto (sem gerar arquivos)' 'check-template: só os checks do template' 'app-setup: cria .venv e instala dependências do produto (rede)' 'app-lint / app-test: lint e testes do produto' 'e2e-setup / e2e: Chromium (rede, uma vez) e testes de teclado/foco' 'run: catálogo em http://127.0.0.1:5000'
setup:
	bash scripts/setup.sh
doctor:
	bash scripts/doctor.sh
sdd:
	bash scripts/sdd/spec-lint-all.sh
	bash scripts/sdd/spec-index.sh
	bash scripts/sdd/spec-drift.sh
lint:
	bash scripts/sdd/spec-lint-all.sh
	@find scripts .claude/hooks -name '*.sh' -exec bash -n {} \;
	python3 -m json.tool .claude/settings.json >/dev/null
test:
	PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/tests -p 'test_*.py' -v
check-template: lint
	bash scripts/sdd/spec-drift.sh
	$(MAKE) test
check: check-template app-lint app-test

.PHONY: test-mutations
test-mutations:
	PYTHONDONTWRITEBYTECODE=1 python3 scripts/tests/mutation_checks.py

# Produto (ADR-002). VENV pode apontar para outro ambiente: make check VENV=/caminho/.venv
VENV ?= .venv
PY = $(VENV)/bin/python

.PHONY: app-setup app-venv app-lint app-test e2e-setup e2e run
app-setup:
	python3 -m venv $(VENV)
	$(PY) -m pip install -r requirements-dev.txt
app-venv:
	@test -x $(PY) || { echo "Ambiente do produto ausente em $(VENV): rode make app-setup" >&2; exit 1; }
app-lint: app-venv
	$(PY) -m ruff check catalogo tests
	$(PY) -m ruff format --check catalogo tests
app-test: app-venv
	PYTHONDONTWRITEBYTECODE=1 $(PY) -m pytest tests --ignore=tests/e2e -p no:cacheprovider
e2e-setup: app-venv
	$(PY) -m playwright install chromium
e2e: app-venv
	PYTHONDONTWRITEBYTECODE=1 $(PY) -m pytest tests/e2e -p no:cacheprovider
run: app-venv
	$(PY) -m catalogo
