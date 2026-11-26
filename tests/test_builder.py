from pathlib import Path

from danfse.builder import build_data
from danfse.parser import parse

FIXTURES = Path(__file__).parent / "fixtures"


def _data(nome="nfse_exemplo.xml"):
    return build_data(parse((FIXTURES / nome).read_bytes())["NFSe"])


def test_chave_acesso_strips_nfs_prefix():
    chave = _data()["chave_acesso"]
    assert not chave.startswith("NFS")
    assert len(chave) == 50
    assert chave.isdigit()
    assert chave.startswith("4106902")  # Curitiba (IBGE)


def test_cabecalho():
    data = _data()
    assert data["numero_nfse"] == "1091"
    assert data["numero_dps"] == "800000813"
    assert data["serie_dps"] == "2026"
    assert data["situacao"] == "NFS-e Emitida"
    assert data["ambiente"] == 1  # tpAmb = 1 (produção)
    assert data["tipo_ambiente"] == "1 - Produção"
    assert data["ambiente_gerador"] == "2 - Fisco"


def test_emitente():
    emit = _data()["emitente"]
    assert emit["nome"] == "PRESTADORA DE SERVICOS EXEMPLO LTDA"
    assert emit["cnpj_cpf"] == "11.222.333/0001-81"
    assert emit["municipio"] == "Curitiba / PR"
    assert "ME/EPP" in emit["simples_nacional"]


def test_tomador():
    toma = _data()["tomador"]
    assert toma is not None
    assert toma["nome"] == "TOMADOR EXEMPLO LTDA"
    assert toma["cnpj_cpf"] == "44.555.666/0001-72"
    assert toma["municipio"] == "Curitiba / PR"


def test_servico_e_totais():
    data = _data()
    assert data["servico"]["codigo_trib_nac_mun"] == "01.05.01 / 001"
    assert "LICENCIAMENTO" in data["servico"]["descricao"].upper()
    assert data["totais"]["valor_servico"] == "R$ 117,60"
    assert data["totais"]["valor_liquido"] == "R$ 117,60"


def test_tributacao_municipal_presente():
    tm = _data()["tributacao_municipal"]
    assert tm is not None
    assert tm["tributacao_issqn"] == "Operação Tributável"
    assert tm["retencao_issqn"] == "Não Retido"


def test_municipio_emissao():
    assert _data()["municipio_emissao"] == "Município: Curitiba / PR"


def test_grupos_opcionais_ausentes_sao_none():
    data = _data()
    assert data["intermediario"] is None
    assert data["destinatario"] is None
    assert data["tributacao_ibscbs"] is None


def test_tomador_pessoa_fisica_cpf():
    data = _data("nfse_tomador_cpf.xml")
    toma = data["tomador"]
    assert toma is not None
    assert toma["nome"] == "FULANO DE TAL"
    assert toma["cnpj_cpf"] == "123.456.789-09"
    assert "MEI" in data["emitente"]["simples_nacional"]
    assert data["tributacao_municipal"]["retencao_issqn"] == "Retido pelo Tomador"


def test_sem_tomador():
    data = _data("nfse_sem_tomador.xml")
    assert data["tomador"] is None
    assert data["emitente"]["simples_nacional"] == "Não Optante"
    assert data["totais"]["valor_servico"] == "R$ 2.500,00"
