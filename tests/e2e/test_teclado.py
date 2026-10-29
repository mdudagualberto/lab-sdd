"""F-CATALOGO-V1 AC-8: teclado e foco num navegador real."""

FOCO_ID = "document.activeElement && document.activeElement.id"


def foco_texto(pagina):
    return pagina.evaluate("document.activeElement.textContent.trim()")


def test_ac8_tab_vai_do_topo_ao_campo_e_depois_ao_botao(pagina, servidor):
    pagina.goto(servidor)

    pagina.keyboard.press("Tab")
    assert pagina.evaluate(FOCO_ID) == "ano"

    pagina.keyboard.press("Tab")
    assert pagina.evaluate("document.activeElement.tagName") == "BUTTON"
    assert foco_texto(pagina) == "Filtrar"


def test_ac8_enter_no_campo_aplica_o_filtro(pagina, servidor):
    pagina.goto(servidor)
    pagina.keyboard.press("Tab")
    pagina.keyboard.type("2024")

    with pagina.expect_navigation():
        pagina.keyboard.press("Enter")

    assert "ano=2024" in pagina.url
    assert pagina.locator("#contador").inner_text() == "Artigos exibidos: 3"
    assert pagina.locator("#artigos li").count() == 3


def test_ac8_apos_entrada_invalida_com_enter_o_foco_esta_no_campo(pagina, servidor):
    pagina.goto(servidor)
    pagina.keyboard.press("Tab")
    pagina.keyboard.type("abc")

    with pagina.expect_navigation():
        pagina.keyboard.press("Enter")

    assert (
        pagina.locator("#erro-ano").inner_text() == "Informe um ano com quatro dígitos"
    )
    assert pagina.evaluate(FOCO_ID) == "ano"
