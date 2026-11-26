"""Lookup de municípios pelo código IBGE (7 dígitos).

Dados de domínio público do IBGE. ``lookup(cmun)`` devolve ``"Nome / UF"`` ou,
quando o código não é encontrado, o próprio código (comportamento do original PHP
``Municipios::lookup``).
"""
from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources


@lru_cache(maxsize=1)
def _map() -> dict:
    with resources.files("danfse.data").joinpath("municipios.json").open(
        "r", encoding="utf-8"
    ) as fh:
        data = json.load(fh)
    return {str(item["id"]): (item["nome"], item["uf"]) for item in data}


def lookup(cmun) -> str:
    code = str(cmun or "").strip()
    if not code:
        return ""
    found = _map().get(code)
    if found is None:
        return code
    nome, uf = found
    return f"{nome} / {uf}"
