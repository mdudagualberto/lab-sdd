"""F-SETUP-V1 AC-4 / DS-00: só a camada web importa Flask ou Jinja."""

import ast
from pathlib import Path

PACOTE = Path(__file__).resolve().parent.parent / "catalogo"
CAMADA_WEB = {"web.py", "__main__.py"}
PROIBIDOS = {"flask", "jinja2"}


def imports_proibidos(arquivo: Path) -> set[str]:
    return imports_de(arquivo) & PROIBIDOS


def test_dominio_nao_importa_flask_nem_jinja():
    violacoes = {
        arquivo.relative_to(PACOTE.parent).as_posix(): sorted(proibidos)
        for arquivo in sorted(PACOTE.rglob("*.py"))
        if arquivo.name not in CAMADA_WEB and (proibidos := imports_proibidos(arquivo))
    }
    assert not violacoes, (
        f"DS-00 R1: só {sorted(CAMADA_WEB)} podem importar {sorted(PROIBIDOS)}; "
        f"violações: {violacoes}. Mova a dependência para a camada web ou "
        "registre uma ADR para mudar a fronteira."
    )


def test_so_dados_le_o_formato_json():
    leitores = sorted(
        arquivo.relative_to(PACOTE.parent).as_posix()
        for arquivo in PACOTE.rglob("*.py")
        if arquivo.name != "dados.py" and "json" in imports_de(arquivo)
    )
    assert not leitores, (
        "DS-00 R2: o formato dos artigos tem fonte única em catalogo/dados.py; "
        f"estes módulos importam json: {leitores}"
    )


def imports_de(arquivo: Path) -> set[str]:
    nomes = set()
    for no in ast.walk(ast.parse(arquivo.read_text(encoding="utf-8"))):
        if isinstance(no, ast.Import):
            nomes |= {alias.name.split(".")[0] for alias in no.names}
        elif isinstance(no, ast.ImportFrom) and no.module and no.level == 0:
            nomes.add(no.module.split(".")[0])
    return nomes
