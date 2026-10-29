"""Camada web: única parte do pacote que conhece Flask (DS-00)."""

from pathlib import Path

from flask import Flask, render_template

from catalogo.dados import carregar_artigos

DADOS_PADRAO = Path(__file__).resolve().parent.parent / "data" / "artigos.json"


def create_app(caminho_dados: Path | None = None) -> Flask:
    artigos = carregar_artigos(caminho_dados or DADOS_PADRAO)
    app = Flask(__name__)

    @app.get("/")
    def inicio():
        return render_template("catalogo.html", artigos=artigos)

    return app
