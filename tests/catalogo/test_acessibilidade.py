"""F-CATALOGO-V1 AC-7: rótulo, aria-invalid, aria-describedby e foco no erro."""


def test_ac7_campo_tem_rotulo_visivel_associado(abrir):
    pagina = abrir()
    rotulo = pagina.html.select_one("label[for=ano]")

    assert rotulo is not None
    assert rotulo.get_text(strip=True) == "Ano de publicação"
    assert pagina.campo["id"] == "ano"


def test_ac7_estado_de_erro_marca_o_campo_e_aponta_a_mensagem(abrir):
    pagina = abrir(ano="abc", aplicado="")
    campo = pagina.campo
    mensagem = pagina.html.select_one("#erro-ano")

    assert campo.get("aria-invalid") == "true"
    assert campo.has_attr("autofocus")
    assert mensagem is not None
    assert mensagem["id"] in campo["aria-describedby"].split()
    assert mensagem.get("role") == "alert"


def test_ac7_fora_do_erro_nao_ha_marcacao_de_erro(abrir):
    for pagina in (
        abrir(),
        abrir(ano="2024", aplicado=""),
        abrir(ano="1999", aplicado=""),
    ):
        campo = pagina.campo
        assert not campo.has_attr("aria-invalid")
        assert not campo.has_attr("autofocus")
        assert pagina.erro is None
        assert "erro-ano" not in campo.get("aria-describedby", "").split()


def test_ac7_ajuda_descreve_o_campo_em_todos_os_estados(abrir):
    for pagina in (abrir(), abrir(ano="abc", aplicado="")):
        ajuda = pagina.html.select_one("#ajuda-ano")
        assert ajuda is not None
        assert "ajuda-ano" in pagina.campo["aria-describedby"].split()
