"""Servidor local com a fixture e navegador Chromium headless para os testes e2e."""

import threading

import pytest
from playwright.sync_api import sync_playwright
from werkzeug.serving import make_server

from catalogo.web import create_app
from tests.conftest import FIXTURE


@pytest.fixture(scope="session")
def servidor():
    servidor = make_server("127.0.0.1", 0, create_app(FIXTURE))
    thread = threading.Thread(target=servidor.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{servidor.server_port}/"
    servidor.shutdown()


@pytest.fixture(scope="session")
def navegador():
    with sync_playwright() as playwright:
        navegador = playwright.chromium.launch()
        yield navegador
        navegador.close()


@pytest.fixture
def pagina(navegador):
    contexto = navegador.new_context(viewport={"width": 1280, "height": 800})
    yield contexto.new_page()
    contexto.close()
