"""Leitura da página renderizada para os testes das ACs da F-CATALOGO-V1."""

import json

import pytest
from bs4 import BeautifulSoup

from tests.conftest import FIXTURE


class Pagina:
    def __init__(self, html: bytes):
        self.html = BeautifulSoup(html, "html.parser")

    def _texto(self, seletor):
        elemento = self.html.select_one(seletor)
        return elemento.get_text(" ", strip=True) if elemento else None

    @property
    def titulos(self):
        return [
            li.select_one(".titulo").get_text(strip=True)
            for li in self.html.select("#artigos li")
        ]

    @property
    def contador(self):
        return self._texto("#contador")

    @property
    def vazio(self):
        return self._texto("#vazio")

    @property
    def erro(self):
        return self._texto("#erro-ano")

    @property
    def campo(self):
        return self.html.select_one("input#ano")

    @property
    def aplicado(self):
        return self.html.select_one("input[name=aplicado]")["value"]


@pytest.fixture
def abrir(client):
    def abrir(**parametros):
        resposta = client.get("/", query_string=parametros)
        assert resposta.status_code == 200
        return Pagina(resposta.data)

    return abrir


@pytest.fixture
def esperado():
    """Oráculo independente da aplicação: títulos da fixture por ano, em ordem."""
    registros = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def esperado(ano=None):
        return [r["titulo"] for r in registros if ano is None or r["ano"] == ano]

    return esperado
