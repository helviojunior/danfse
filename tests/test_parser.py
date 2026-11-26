from pathlib import Path

import pytest

from danfse.errors import XmlInvalidoError
from danfse.parser import parse

FIXTURE = Path(__file__).parent / "fixtures" / "nfse_exemplo.xml"


def _tree():
    return parse(FIXTURE.read_bytes())


def test_root_is_nfse():
    tree = _tree()
    assert "NFSe" in tree
    assert isinstance(tree["NFSe"], dict)


def test_infnfse_attributes_and_fields():
    inf = _tree()["NFSe"]["infNFSe"]
    assert inf["@Id"].startswith("NFS")
    assert inf["nNFSe"] == "1091"
    assert inf["emit"]["CNPJ"] == "11222333000181"
    assert inf["emit"]["enderNac"]["UF"] == "PR"


def test_nested_dps_toma():
    inf_dps = _tree()["NFSe"]["infNFSe"]["DPS"]["infDPS"]
    assert inf_dps["serie"] == "2026"
    assert inf_dps["toma"]["xNome"] == "TOMADOR EXEMPLO LTDA"
    assert inf_dps["toma"]["end"]["endNac"]["CEP"] == "80020000"


def test_fixture_sanitizado_sem_assinatura():
    # Fixtures públicos não podem conter assinaturas/certificados reais.
    raw = FIXTURE.read_text(encoding="utf-8")
    assert "Signature" not in raw
    assert "X509Certificate" not in raw


def test_invalid_xml_raises():
    with pytest.raises(XmlInvalidoError):
        parse("<nfse><broken>")
