"""F-SETUP-V1 AC-3: `make check` reprova quando um teste do produto falha."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
# Só existe na cópia temporária; uma variável de ambiente poderia ser exportada
# por engano e pular o controle em silêncio.
MARCADOR = ".catalogo-teste-interno"

pytestmark = pytest.mark.skipif(
    (RAIZ / MARCADOR).exists(),
    reason="execução interna de make check; evita recursão (risco R-1)",
)


@pytest.fixture
def copia(tmp_path):
    destino = tmp_path / "repo"
    shutil.copytree(
        RAIZ,
        destino,
        ignore=shutil.ignore_patterns(
            ".venv", "__pycache__", ".pytest_cache", ".ruff_cache"
        ),
    )
    (destino / MARCADOR).write_text("cópia de tests/test_comandos.py\n")
    return destino


def make_check(copia):
    return subprocess.run(
        # O mesmo ambiente que roda esta suíte, mesmo com make check VENV=...
        ["make", "check", f"VENV={sys.prefix}"],
        cwd=copia,
        env=dict(os.environ),
        capture_output=True,
        text=True,
        timeout=600,
    )


def test_make_check_verde_e_vermelho_com_teste_do_produto(copia):
    verde = make_check(copia)
    assert verde.returncode == 0, verde.stdout[-3000:] + verde.stderr[-3000:]

    falha = copia / "tests" / "test_falha_proposital.py"
    falha.write_text("def test_falha_proposital():\n    assert 1 + 1 == 3\n")
    vermelho = make_check(copia)

    assert vermelho.returncode != 0, vermelho.stdout[-3000:]
    assert "FAILED tests/test_falha_proposital.py" in vermelho.stdout
