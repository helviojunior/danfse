"""Mapas de rótulos dos códigos do leiaute da NFS-e Nacional.

Port dos enums de ``src/Danfse/Enums`` (guilhermecfviana/danfse-nacional, MIT).
Cada ``label_for`` recebe o valor cru do XML (string) e devolve o rótulo humano,
ou ``"-"`` quando o código é vazio/desconhecido.
"""
from __future__ import annotations


def _label(mapping: dict, value, default: str = "-") -> str:
    key = str(value or "").strip()
    if key == "":
        return default
    return mapping.get(key, default)


OP_SIMP_NAC = {
    "1": "Não Optante",
    "2": "Optante - Microempreendedor Individual (MEI)",
    "3": "Optante - Microempresa ou Empresa de Pequeno Porte (ME/EPP)",
}

REG_AP_TRIB_SN = {
    "1": "Regime de apuração dos tributos federais e municipal pelo Simples Nacional",
    "2": (
        "Regime de apuração dos tributos federais pelo SN e o ISSQN pela NFS-e "
        "conforme respectiva legislação municipal do tributo"
    ),
    "3": (
        "Regime de apuração dos tributos federais e municipal pela NFS-e conforme "
        "respectivas legislações federal e municipal de cada tributo"
    ),
}

REG_ESP_TRIB = {
    "0": "Nenhum",
    "1": "Ato Cooperado (Cooperativa)",
    "2": "Estimativa",
    "3": "Microempresa Municipal",
    "4": "Notário ou Registrador",
    "5": "Profissional Autônomo",
    "6": "Sociedade de Profissionais",
}

TRIB_ISSQN = {
    "1": "Operação Tributável",
    "2": "Imunidade",
    "3": "Exportação de Serviço",
    "4": "Não Incidência",
}

TP_RET_ISSQN = {
    "1": "Não Retido",
    "2": "Retido pelo Tomador",
    "3": "Retido pelo Intermediário",
}

TP_RET_PIS_COFINS = {
    "0": "0 - PIS/COFINS/CSLL Não Retidos",
    "1": "1 - PIS/COFINS Retido",
    "2": "2 - PIS/COFINS Não Retido",
    "3": "3 - PIS/COFINS/CSLL Retidos",
    "4": "4 - PIS/COFINS Retidos, CSLL Não Retido",
    "5": "5 - PIS Retido, COFINS/CSLL Não Retido",
    "6": "6 - COFINS Retido, PIS/CSLL Não Retido",
    "7": "7 - PIS Não Retido, COFINS/CSLL Retidos",
    "8": "8 - PIS/COFINS Não Retidos, CSLL Retido",
    "9": "9 - COFINS Não Retido, PIS/CSLL Retidos",
}

AMB_GER = {
    "1": "1 - Contribuinte",
    "2": "2 - Fisco",
    "3": "3 - Contribuinte c/ Fisco",
    "4": "4 - Terceiro",
}

TP_AMB = {
    "1": "1 - Produção",
    "2": "2 - Homologação",
}

EMITENTE_NFSE = {
    "1": "Prestador do Serviço",
    "2": "Tomador do Serviço",
    "3": "Intermediário do Serviço",
}

FINALIDADE = {
    "0": "NFS-e regular",
    "1": "NFS-e de crédito",
    "2": "NFS-e de débito",
}


def op_simp_nac(value) -> str:
    return _label(OP_SIMP_NAC, value)


def reg_ap_trib_sn(value) -> str:
    return _label(REG_AP_TRIB_SN, value)


def reg_esp_trib(value) -> str:
    return _label(REG_ESP_TRIB, value)


def trib_issqn(value) -> str:
    return _label(TRIB_ISSQN, value)


def tp_ret_issqn(value) -> str:
    return _label(TP_RET_ISSQN, value)


def tp_ret_pis_cofins(value) -> str:
    return _label(TP_RET_PIS_COFINS, value)


def amb_ger(value) -> str:
    v = str(value or "").strip()
    return AMB_GER.get(v, v if v else "-")


def tp_amb(value) -> str:
    v = str(value or "").strip()
    return TP_AMB.get(v, v if v else "-")


def emitente_nfse(value) -> str:
    return _label(EMITENTE_NFSE, value)


def finalidade(value) -> str:
    return _label(FINALIDADE, value)
