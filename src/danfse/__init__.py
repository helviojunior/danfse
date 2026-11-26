"""danfse — gerador da DANFSe (NFS-e Nacional) em PDF a partir do XML.

Uso rápido::

    from danfse import generate

    pdf = generate("nota.xml")                 # caminho, string XML ou bytes
    with open("danfse.pdf", "wb") as fh:
        fh.write(pdf)
"""
from __future__ import annotations

from .__about__ import __version__
from .errors import CampoObrigatorioError, DanfseError, XmlInvalidoError
from .generator import generate, generate_from_file, generate_from_string
from .options import Options

__all__ = [
    "__version__",
    "generate",
    "generate_from_file",
    "generate_from_string",
    "Options",
    "DanfseError",
    "XmlInvalidoError",
    "CampoObrigatorioError",
]
