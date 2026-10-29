"""F-CATALOGO-V1 AC-5 (erro preserva o resultado anterior) e AC-6 (erro some)."""

import pytest

MENSAGEM = "Informe um ano com quatro dígitos"
INVALIDAS = [
    "abc",  # texto
    "202",  # três dígitos
    "20245",  # cinco dígitos
    "２０２４",  # dígitos de largura total (não ASCII)
    "٢٠٢٤",  # dígitos arábico-índicos (não ASCII)
    "+2024",  # sinal
    "20 24",  # espaço interno
    "2024.0",  # decimal
    "<b>2024</b>",  # marcação
]


@pytest.mark.parametrize("texto", INVALIDAS)
def test_ac5_erro_preserva_filtro_anterior(abrir, esperado, texto):
    antes = abrir(ano="2024", aplicado="")
    depois = abrir(ano=texto, aplicado=antes.aplicado)

    assert depois.erro == MENSAGEM
    assert depois.titulos == antes.titulos == esperado("2024")
    assert depois.contador == antes.contador == "Artigos exibidos: 3"
    assert depois.campo["value"] == texto
    assert depois.aplicado == "2024"


@pytest.mark.parametrize("texto", ["abc", " 20245 "])
def test_ac5_erro_a_partir_do_estado_inicial_mantem_todos(abrir, esperado, texto):
    pagina = abrir(ano=texto)

    assert pagina.erro == MENSAGEM
    assert pagina.titulos == esperado()
    assert pagina.campo["value"] == texto


@pytest.mark.parametrize("adulterado", ["abc", "<script>", "٢٠٢٤"])
def test_ac5_aplicado_adulterado_vale_todos(abrir, esperado, adulterado):
    pagina = abrir(ano="xyz", aplicado=adulterado)

    assert pagina.erro == MENSAGEM
    assert pagina.titulos == esperado()
    assert pagina.aplicado == ""


def test_ac5_texto_digitado_aparece_escapado(client):
    html = client.get("/", query_string={"ano": '"><script>x</script>'}).data

    assert b"<script>x</script>" not in html
    assert b"&lt;script&gt;" in html


@pytest.mark.parametrize(
    ("ano", "titulos_de"),
    [("2023", "2023"), ("", None), ("  ", None), ("1999", "1999")],
)
def test_ac6_proxima_aplicacao_valida_remove_o_erro(abrir, esperado, ano, titulos_de):
    com_erro = abrir(ano="abc", aplicado="2024")
    assert com_erro.erro == MENSAGEM

    depois = abrir(ano=ano, aplicado=com_erro.aplicado)

    assert depois.erro is None
    assert depois.titulos == esperado(titulos_de)
