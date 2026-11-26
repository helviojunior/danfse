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
    assert inf["emit"]["CNPJ"] == "40569411000117"
    assert inf["emit"]["enderNac"]["UF"] == "MG"


def test_nested_dps_toma():
    inf_dps = _tree()["NFSe"]["infNFSe"]["DPS"]["infDPS"]
    assert inf_dps["serie"] == "2026"
    assert inf_dps["toma"]["xNome"] == "TESTE LTDA"
    assert inf_dps["toma"]["end"]["endNac"]["CEP"] == "30140128"


def test_invalid_xml_raises():
    with pytest.raises(XmlInvalidoError):
        parse("<nfse><broken>")
