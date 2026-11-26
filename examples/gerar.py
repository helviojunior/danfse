"""Exemplo mínimo: gera a DANFSe a partir do XML de exemplo e grava um PDF.

Uso:
    python examples/gerar.py [caminho_do_xml] [saida.pdf]
"""
import sys
from pathlib import Path

from danfse import generate

RAIZ = Path(__file__).resolve().parent.parent
XML_PADRAO = RAIZ / "tests" / "fixtures" / "nfse_exemplo.xml"


def main() -> None:
    xml = Path(sys.argv[1]) if len(sys.argv) > 1 else XML_PADRAO
    saida = Path(sys.argv[2]) if len(sys.argv) > 2 else RAIZ / "danfse.pdf"
    pdf = generate(str(xml))
    saida.write_bytes(pdf)
    print(f"DANFSe gerada: {saida} ({len(pdf)} bytes)")


if __name__ == "__main__":
    main()
