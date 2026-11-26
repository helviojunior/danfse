"""Interface de linha de comando: ``danfse nota.xml -o saida.pdf``."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .__about__ import __version__
from .errors import DanfseError
from .generator import generate_from_file
from .options import WATERMARKS, Options


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="danfse",
        description="Gera a DANFSe (PDF) da NFS-e Nacional a partir do XML.",
    )
    parser.add_argument("xml", help="Caminho do arquivo XML da NFS-e.")
    parser.add_argument(
        "-o",
        "--output",
        help="Caminho do PDF de saída (padrão: XML com extensão .pdf).",
    )
    parser.add_argument(
        "--watermark",
        choices=WATERMARKS,
        help="Marca d'água: cancelada ou substituida.",
    )
    parser.add_argument("--logo", help="Caminho de uma imagem para substituir o logo.")
    parser.add_argument("--footer", default="", help="Texto de rodapé em todas as páginas.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv=None) -> int:
    args = _build_parser().parse_args(argv)
    xml_path = Path(args.xml)
    if not xml_path.exists():
        print(f"Arquivo não encontrado: {xml_path}", file=sys.stderr)
        return 2
    output = Path(args.output) if args.output else xml_path.with_suffix(".pdf")
    options = Options(
        output="file",
        output_path=str(output),
        watermark=args.watermark,
        logo=args.logo,
        footer_text=args.footer,
    )
    try:
        generate_from_file(xml_path, options)
    except DanfseError as exc:
        print(f"Erro ao gerar a DANFSe: {exc}", file=sys.stderr)
        return 1
    print(str(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
