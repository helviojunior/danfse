"""Orquestra a geração da DANFSe: XML -> dados -> HTML -> PDF (WeasyPrint)."""
from __future__ import annotations

import base64
import mimetypes
from functools import lru_cache
from importlib import resources
from pathlib import Path

from .builder import build_data
from .options import Options
from .parser import parse
from .qrcode_util import qr_data_uri
from .templating import render

TEMPLATE = "danfse.html"
XmlInput = str | bytes


@lru_cache(maxsize=1)
def _default_logo_data_uri() -> str:
    data = resources.files("danfse.assets.logos").joinpath("nfse.png").read_bytes()
    return "data:image/png;base64," + base64.b64encode(data).decode("ascii")


def _logo_data_uri(logo: str | None) -> str:
    if not logo:
        return _default_logo_data_uri()
    path = Path(logo)
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    data = path.read_bytes()
    return f"data:{mime};base64," + base64.b64encode(data).decode("ascii")


def _read_input(xml_input: XmlInput) -> bytes:
    if isinstance(xml_input, (bytes, bytearray)):
        return bytes(xml_input)
    text = str(xml_input)
    if "<" in text:  # parece XML inline
        return text.encode("utf-8")
    path = Path(text)
    if path.exists():
        return path.read_bytes()
    return text.encode("utf-8")


def _render_html(xml_bytes: bytes, options: Options) -> str:
    tree = parse(xml_bytes)
    nfse = tree.get("NFSe") or (next(iter(tree.values()), {}) if tree else {})
    if not isinstance(nfse, dict):
        nfse = {}
    data = build_data(nfse)
    data["watermark_status"] = options.watermark
    data["watermark_text"] = options.watermark_text()
    return render(
        TEMPLATE,
        data=data,
        qr_code=qr_data_uri(data["chave_acesso"]),
        logo=_logo_data_uri(options.logo),
        municipality=options.municipality,
        footer_text=options.footer_text,
    )


def _to_pdf(html: str) -> bytes:
    # Import tardio: WeasyPrint depende de libs nativas e é a dependência mais
    # pesada; importar aqui mantém o import do pacote leve e barato.
    from weasyprint import HTML

    return HTML(string=html).write_pdf()


def generate_from_string(xml_content: XmlInput, options=None) -> bytes:
    """Gera a DANFSe a partir do conteúdo XML (str ou bytes)."""
    options = Options.coerce(options)
    xml_bytes = xml_content if isinstance(xml_content, (bytes, bytearray)) else str(xml_content).encode("utf-8")
    pdf = _to_pdf(_render_html(bytes(xml_bytes), options))
    if options.output == "file" and options.output_path:
        Path(options.output_path).write_bytes(pdf)
    return pdf


def generate_from_file(path: str | Path, options=None) -> bytes:
    """Gera a DANFSe a partir de um arquivo XML."""
    return generate_from_string(Path(path).read_bytes(), options)


def generate(xml_input: XmlInput, options=None) -> bytes:
    """Gera a DANFSe. ``xml_input`` pode ser um caminho de arquivo, uma string
    XML ou bytes XML (autodetectado, como no projeto de referência)."""
    options = Options.coerce(options)
    return generate_from_string(_read_input(xml_input), options)
