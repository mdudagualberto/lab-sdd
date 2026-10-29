"""Carga validada dos artigos do arquivo JSON local (fonte única do formato)."""

import json
import re
from dataclasses import dataclass
from pathlib import Path

ANO = re.compile(r"[0-9]{4}")


class ErroDados(ValueError):
    """Arquivo de artigos inválido; a mensagem cita registro e campo."""


@dataclass(frozen=True)
class Artigo:
    titulo: str
    autores: tuple[str, ...]
    ano: int


def carregar_artigos(caminho: Path) -> list[Artigo]:
    try:
        registros = json.loads(Path(caminho).read_text(encoding="utf-8"))
    except json.JSONDecodeError as erro:
        raise ErroDados(f"{caminho}: JSON malformado ({erro})") from erro
    if not isinstance(registros, list):
        raise ErroDados(f"{caminho}: esperada uma lista JSON de artigos")
    return [_artigo(caminho, indice, r) for indice, r in enumerate(registros)]


def _artigo(caminho: Path, indice: int, registro: object) -> Artigo:
    def invalido(campo: str, regra: str) -> ErroDados:
        return ErroDados(f"{caminho}: registro {indice}, campo {campo}: {regra}")

    if not isinstance(registro, dict):
        raise invalido("(registro)", "esperado um objeto")
    titulo = registro.get("titulo")
    if not isinstance(titulo, str) or not titulo.strip():
        raise invalido("titulo", "texto não vazio obrigatório")
    autores = registro.get("autores")
    if (
        not isinstance(autores, list)
        or not autores
        or not all(isinstance(a, str) and a.strip() for a in autores)
    ):
        raise invalido("autores", "lista não vazia de nomes obrigatória")
    ano = registro.get("ano")
    if not isinstance(ano, str) or not ANO.fullmatch(ano):
        raise invalido("ano", "string de exatamente quatro dígitos de 0 a 9")
    return Artigo(titulo, tuple(autores), int(ano))
