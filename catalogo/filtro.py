"""Regra do filtro por ano (puro, sem Flask; DS-00)."""

from dataclasses import dataclass

from catalogo.dados import ANO, Artigo


@dataclass(frozen=True)
class Entrada:
    texto: str
    ano: int | None
    valida: bool


def interpretar_entrada(texto: str | None) -> Entrada:
    """Vazio após strip = sem filtro; quatro dígitos ASCII = ano; o resto é inválido."""
    limpo = (texto or "").strip()
    if not limpo:
        return Entrada(limpo, None, True)
    if ANO.fullmatch(limpo):
        return Entrada(limpo, int(limpo), True)
    return Entrada(limpo, None, False)


def filtrar(artigos: list[Artigo], ano: int | None) -> list[Artigo]:
    return [artigo for artigo in artigos if ano is None or artigo.ano == ano]
