"""F-CATALOGO-V1 AC-4: ano válido sem artigos mostra a mensagem de lista vazia."""

import pytest


@pytest.mark.parametrize("ano", ["1999", "0000", "9999"])
def test_ac4_ano_valido_sem_artigos(abrir, ano):
    pagina = abrir(ano=ano, aplicado="")

    assert pagina.vazio == "Nenhum artigo encontrado"
    assert pagina.titulos == []
    assert pagina.html.select("#artigos li") == []
    assert pagina.contador == "Artigos exibidos: 0"
    assert pagina.erro is None


def test_ac4_lista_com_resultados_nao_mostra_mensagem_de_vazio(abrir):
    assert abrir(ano="2024", aplicado="").vazio is None
