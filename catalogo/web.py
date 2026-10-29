"""Camada web: única parte do pacote que conhece Flask (DS-00)."""

from pathlib import Path

from flask import Flask, render_template, request

from catalogo.dados import carregar_artigos
from catalogo.filtro import filtrar, interpretar_entrada

DADOS_PADRAO = Path(__file__).resolve().parent.parent / "data" / "artigos.json"


def create_app(caminho_dados: Path | None = None) -> Flask:
    artigos = carregar_artigos(caminho_dados or DADOS_PADRAO)
    app = Flask(__name__)

    @app.get("/")
    def inicio():
        digitado = request.args.get("ano", "")
        entrada = interpretar_entrada(digitado)
        erro = not entrada.valida
        if erro:
            # Mantém o último filtro válido (D-6); "aplicado" adulterado vale "todos".
            entrada = interpretar_entrada(request.args.get("aplicado", ""))
            if not entrada.valida:
                entrada = interpretar_entrada("")
        return render_template(
            "catalogo.html",
            artigos=filtrar(artigos, entrada.ano),
            digitado=digitado,
            aplicado=entrada.texto,
            erro=erro,
        )

    return app
