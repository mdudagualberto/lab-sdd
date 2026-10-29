"""F-SETUP-V1 AC-2: carga validada do arquivo de artigos."""

import json

import pytest

from catalogo.dados import Artigo, ErroDados, carregar_artigos
from catalogo.web import create_app

VALIDO = {"titulo": "Um artigo", "autores": ["Autora Fictícia"], "ano": "2024"}


def gravar(tmp_path, conteudo):
    caminho = tmp_path / "artigos.json"
    texto = conteudo if isinstance(conteudo, str) else json.dumps(conteudo)
    caminho.write_text(texto, encoding="utf-8")
    return caminho


def test_carrega_artigos_validos_na_ordem_do_arquivo(tmp_path):
    segundo = {"titulo": "Outro", "autores": ["A", "B"], "ano": "1999"}
    caminho = gravar(tmp_path, [VALIDO, segundo])

    assert carregar_artigos(caminho) == [
        Artigo("Um artigo", ("Autora Fictícia",), 2024),
        Artigo("Outro", ("A", "B"), 1999),
    ]


def test_json_malformado(tmp_path):
    with pytest.raises(ErroDados, match="JSON"):
        carregar_artigos(gravar(tmp_path, '[{"titulo": '))


@pytest.mark.parametrize(
    ("alteracao", "campo"),
    [
        ({"titulo": None}, "titulo"),
        ({"autores": None}, "autores"),
        ({"ano": None}, "ano"),
        ({"autores": []}, "autores"),
        ({"ano": "24"}, "ano"),
        ({"ano": "20245"}, "ano"),
        ({"ano": "２０２４"}, "ano"),
        ({"ano": "٢٠٢٤"}, "ano"),
        ({"ano": 2024}, "ano"),
    ],
)
def test_registro_invalido_cita_indice_e_campo(tmp_path, alteracao, campo):
    invalido = {k: v for k, v in {**VALIDO, **alteracao}.items() if v is not None}
    caminho = gravar(tmp_path, [VALIDO, invalido])

    with pytest.raises(ErroDados) as erro:
        carregar_artigos(caminho)

    assert "registro 1" in str(erro.value)
    assert campo in str(erro.value)


def test_create_app_nao_inicia_com_dados_invalidos(tmp_path):
    caminho = gravar(tmp_path, [{**VALIDO, "ano": 2024}])

    with pytest.raises(ErroDados):
        create_app(caminho)
