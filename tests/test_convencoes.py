"""Ratchets das convenções DS-06 (testes) e DS-07 (nomes)."""

from pathlib import Path

TESTES = Path(__file__).resolve().parent
AUXILIARES = {"conftest.py", "__init__.py"}


def test_arquivos_de_teste_seguem_test_prefixo():
    fora = sorted(
        p.relative_to(TESTES).as_posix()
        for p in TESTES.rglob("*.py")
        if p.name not in AUXILIARES and not p.name.startswith("test_")
    )
    assert not fora, f"DS-07 R2: arquivos de teste se chamam test_*.py; fora: {fora}"


def test_testes_nao_usam_dados_de_demonstracao():
    usam = sorted(
        p.relative_to(TESTES).as_posix()
        for p in TESTES.rglob("*.py")
        if p.name != "test_convencoes.py"
        and (
            "data/artigos.json" in (t := p.read_text(encoding="utf-8"))
            or "DADOS_PADRAO" in t
        )
    )
    assert not usam, (
        "DS-06 R2: testes usam tests/fixtures/artigos.json pela fixture app, "
        f"não os dados de demonstração; violações: {usam}"
    )
