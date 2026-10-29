"""F-SETUP-V1 AC-1: a aplicação sobe com a fixture e responde sem rede."""

from bs4 import BeautifulSoup


def test_pagina_inicial_responde_com_titulo(client):
    resposta = client.get("/")

    assert resposta.status_code == 200
    pagina = BeautifulSoup(resposta.data, "html.parser")
    assert pagina.h1 is not None
    assert pagina.h1.get_text(strip=True) == "Catálogo de artigos"
