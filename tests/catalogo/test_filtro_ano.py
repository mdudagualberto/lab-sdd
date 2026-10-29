"""F-CATALOGO-V1 AC-1 (filtrar por ano) e AC-3 (limpar o filtro)."""

import pytest


def test_ac1_filtra_todos_e_somente_os_artigos_do_ano(abrir, esperado):
    pagina = abrir(ano="2024", aplicado="")

    assert len(esperado("2024")) == 3  # a fixture precisa ter vários de 2024
    assert pagina.titulos == esperado("2024")


def test_ac1_espacos_nas_pontas_dao_o_mesmo_resultado(abrir, esperado):
    assert abrir(ano=" 2024 ", aplicado="").titulos == esperado("2024")


@pytest.mark.parametrize("vazio", ["", "   ", "\t \n"])
def test_ac3_campo_vazio_depois_de_filtrar_mostra_todos(abrir, esperado, vazio):
    assert abrir(ano="2024", aplicado="").titulos == esperado("2024")

    pagina = abrir(ano=vazio, aplicado="2024")

    assert pagina.titulos == esperado()
    assert pagina.erro is None


def test_ac3_estado_inicial_mostra_todos(abrir, esperado):
    assert abrir().titulos == esperado()


def _cliente_com(tmp_path, registros):
    import json

    from catalogo.web import create_app

    caminho = tmp_path / "artigos.json"
    caminho.write_text(json.dumps(registros), encoding="utf-8")
    return create_app(caminho).test_client()


@pytest.mark.parametrize("ano", ["0999", "0000"])
def test_ac1_ano_exibido_mantem_quatro_digitos(tmp_path, ano):
    cliente = _cliente_com(tmp_path, [{"titulo": "T", "autores": ["A"], "ano": ano}])
    html = cliente.get("/", query_string={"ano": ano}).data.decode()

    assert f'<span class="ano">{ano}</span>' in html
