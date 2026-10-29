import socket
from pathlib import Path

import pytest

FIXTURE = Path(__file__).parent / "fixtures" / "artigos.json"


@pytest.fixture
def sem_rede(monkeypatch):
    """Qualquer tentativa de conexão de rede durante o teste falha."""

    def recusar(*args, **kwargs):
        raise AssertionError("acesso à rede durante o teste")

    monkeypatch.setattr(socket.socket, "connect", recusar)
    monkeypatch.setattr(socket, "create_connection", recusar)


@pytest.fixture
def app(sem_rede):
    from catalogo.web import create_app

    return create_app(FIXTURE)


@pytest.fixture
def client(app):
    return app.test_client()
