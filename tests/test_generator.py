"""Testes de ponta a ponta (exigem WeasyPrint com as libs nativas instaladas)."""
import io
from pathlib import Path

import pytest

from danfse import generate, generate_from_file, generate_from_string
from danfse.cli import main

pytest.importorskip("weasyprint")

FIXTURE = Path(__file__).parent / "fixtures" / "nfse_exemplo.xml"


def _assert_pdf(pdf: bytes, min_pages: int = 1):
    assert isinstance(pdf, (bytes, bytearray))
    assert pdf[:4] == b"%PDF"
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(pdf))
    assert len(reader.pages) >= min_pages
    return reader


def test_generate_from_file():
    reader = _assert_pdf(generate_from_file(FIXTURE))
    text = "".join(page.extract_text() or "" for page in reader.pages)
    assert "KRYPTON" in text.upper()
    assert "DANFSE" in text.upper()
    assert "117,60" in text


def test_generate_autodetect_path_and_string():
    _assert_pdf(generate(str(FIXTURE)))
    _assert_pdf(generate(FIXTURE.read_text(encoding="utf-8")))
    _assert_pdf(generate_from_string(FIXTURE.read_bytes()))


def test_watermark_cancelada():
    pdf = generate(str(FIXTURE), {"watermark": "cancelada"})
    reader = _assert_pdf(pdf)
    text = "".join(page.extract_text() or "" for page in reader.pages)
    assert "CANCELADA" in text.upper()


def test_cli_writes_file(tmp_path):
    out = tmp_path / "danfse.pdf"
    rc = main([str(FIXTURE), "-o", str(out)])
    assert rc == 0
    assert out.exists()
    assert out.read_bytes()[:4] == b"%PDF"


def test_output_file_option(tmp_path):
    out = tmp_path / "saida.pdf"
    pdf = generate(str(FIXTURE), {"output": "file", "output_path": str(out)})
    assert out.exists()
    assert out.read_bytes() == pdf
