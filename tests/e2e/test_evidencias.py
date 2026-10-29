"""Capturas por estado e variante para DESIGN-F-CATALOGO-V1 (só com EVIDENCIA=1).

Evidência visual, não prova de teclado ou foco: isso fica em test_teclado.py.
"""

import os
from pathlib import Path

import pytest

DESTINO = Path(__file__).resolve().parents[2] / "docs" / "images"
VARIANTES = {"desktop": (1280, 800), "celular": (375, 800)}
ESTADOS = [
    ("inicial", "", ("desktop", "celular")),
    ("filtrado", "?ano=2024&aplicado=", ("desktop", "celular")),
    ("vazio", "?ano=1999&aplicado=", ("desktop", "celular")),
    ("erro", "?ano=abc&aplicado=", ("desktop", "celular")),
    ("erro-filtrado", "?ano=20245&aplicado=2024", ("desktop",)),
]

pytestmark = pytest.mark.skipif(
    os.environ.get("EVIDENCIA") != "1", reason="capturas só com EVIDENCIA=1"
)


@pytest.mark.parametrize(
    ("estado", "consulta", "variante"),
    [(e, c, v) for e, c, vs in ESTADOS for v in vs],
)
def test_captura_estado(navegador, servidor, estado, consulta, variante):
    largura, altura = VARIANTES[variante]
    contexto = navegador.new_context(viewport={"width": largura, "height": altura})
    pagina = contexto.new_page()
    pagina.goto(servidor + consulta)
    DESTINO.mkdir(parents=True, exist_ok=True)
    pagina.screenshot(
        path=DESTINO / f"F-CATALOGO-V1-{estado}-{variante}.png", full_page=True
    )
    contexto.close()


def test_captura_recuperacao(navegador, servidor):
    contexto = navegador.new_context(viewport={"width": 1280, "height": 800})
    pagina = contexto.new_page()
    pagina.goto(servidor + "?ano=abc&aplicado=")
    pagina.fill("#ano", "2023")
    with pagina.expect_navigation():
        pagina.keyboard.press("Enter")
    assert pagina.locator("#erro-ano").count() == 0
    pagina.screenshot(
        path=DESTINO / "F-CATALOGO-V1-recuperacao-desktop.png", full_page=True
    )
    contexto.close()
