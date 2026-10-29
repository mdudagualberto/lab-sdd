"""F-CATALOGO-V1 AC-2: o contador acompanha os itens visíveis em todos os estados."""

import pytest


@pytest.mark.parametrize(
    "parametros",
    [
        {},  # inicial
        {"ano": "2024", "aplicado": ""},  # filtrado
        {"ano": "2023", "aplicado": "2024"},  # outro filtro
        {"ano": "1999", "aplicado": ""},  # sem resultados
        {"ano": "abc", "aplicado": "2024"},  # após entrada inválida
    ],
)
def test_ac2_contador_igual_a_itens_visiveis(abrir, parametros):
    pagina = abrir(**parametros)

    assert pagina.contador == f"Artigos exibidos: {len(pagina.titulos)}"


def test_ac2_valores_esperados_por_estado(abrir):
    assert abrir().contador == "Artigos exibidos: 8"
    assert abrir(ano="2024", aplicado="").contador == "Artigos exibidos: 3"
    assert abrir(ano="1999", aplicado="").contador == "Artigos exibidos: 0"
