"""Opções de geração da DANFSe."""
from __future__ import annotations

from dataclasses import dataclass, fields

WATERMARKS = ("cancelada", "substituida")


@dataclass
class Options:
    """Opções da geração.

    - ``output``: ``"bytes"`` (padrão, devolve os bytes) ou ``"file"`` (também
      grava em ``output_path``).
    - ``output_path``: caminho do PDF quando ``output="file"``.
    - ``footer_text``: texto de rodapé repetido em todas as páginas.
    - ``watermark``: ``None`` | ``"cancelada"`` | ``"substituida"``.
    - ``logo``: caminho de uma imagem para substituir o logo padrão da NFS-e.
    - ``municipality``: dados opcionais da prefeitura (``name``, ``department``,
      ``email``, ``logo``) exibidos no cabeçalho.
    """

    output: str = "bytes"
    output_path: str | None = None
    footer_text: str = ""
    watermark: str | None = None
    logo: str | None = None
    municipality: dict | None = None

    @classmethod
    def coerce(cls, value) -> Options:
        if value is None:
            return cls()
        if isinstance(value, cls):
            return value
        if isinstance(value, dict):
            allowed = {f.name for f in fields(cls)}
            return cls(**{k: v for k, v in value.items() if k in allowed})
        raise TypeError("options deve ser None, dict ou Options.")

    def watermark_text(self) -> str | None:
        return {"cancelada": "CANCELADA", "substituida": "SUBSTITUÍDA"}.get(
            (self.watermark or "").strip()
        )
