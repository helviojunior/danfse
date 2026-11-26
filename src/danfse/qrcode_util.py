"""Geração do QR Code da DANFSe como data URI (SVG).

O QR aponta para a consulta pública oficial da NFS-e Nacional, igual ao projeto
de referência:
``https://www.nfse.gov.br/ConsultaPublica/?tpc=1&chave={chave}``.
"""
from __future__ import annotations

import segno

CONSULTA_URL = "https://www.nfse.gov.br/ConsultaPublica/?tpc=1&chave={chave}"


def consulta_url(chave_acesso: str) -> str:
    return CONSULTA_URL.format(chave=chave_acesso)


def qr_data_uri(chave_acesso: str, scale: int = 3) -> str:
    """Devolve um data URI SVG com o QR Code da chave de acesso."""
    qr = segno.make(consulta_url(chave_acesso), error="m")
    return qr.svg_data_uri(scale=scale, border=0)
