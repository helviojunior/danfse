"""Monta o dicionário de dados do template a partir da árvore do XML.

Port de ``DanfseTemplate::buildData`` (guilhermecfviana/danfse-nacional, MIT).
Recebe a árvore produzida por :func:`danfse.parser.parse` e devolve o ``data``
consumido pelo template ``danfse.html``.
"""
from __future__ import annotations

from . import enums
from . import formatter as fmt
from .municipios import lookup as muni_lookup

# ---------------------------------------------------------------------------
# Navegação defensiva na árvore de dicts (equivale aos ``?->`` do PHP).
# ---------------------------------------------------------------------------


def _node(obj, *path):
    cur = obj
    for key in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur if isinstance(cur, dict) else None


def _txt(obj, *path, default=""):
    cur = obj
    for key in path:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(key)
        if cur is None:
            return default
    if isinstance(cur, dict):
        return cur.get("#text", default)
    if isinstance(cur, list):
        return default
    return cur


def _doc(node) -> str:
    if not isinstance(node, dict):
        return ""
    for key in ("CNPJ", "CPF", "NIF"):
        value = node.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return ""


def _present(value) -> bool:
    return value is not None and str(value).strip() != ""


def _trim_slash(value: str) -> str:
    return value.strip(" /")


def _join_addr(*parts) -> str:
    return ", ".join(p for p in parts if p)


def _sum_currency(*values) -> str:
    total = 0.0
    has_value = False
    for value in values:
        if _present(value):
            try:
                total += float(value)
                has_value = True
            except (TypeError, ValueError):
                continue
    return fmt.currency(total) if has_value else "-"


def _pct_or_currency(pct, raw_value) -> str:
    """Percentual tem prioridade; senão valor monetário; senão ``-``."""
    if _present(pct) and str(pct).strip() != "0":
        return f"{pct}%"
    if _present(raw_value):
        return fmt.currency(raw_value)
    return "-"


def _codigo_ibge_cep(ibge: str, postal: str) -> str:
    if ibge or postal:
        return _trim_slash(f"{ibge} / {postal}") or "-"
    return "-"


def _municipio(end_nac, end_ext) -> str:
    cmun = _txt(end_nac, "cMun")
    if cmun:
        return muni_lookup(cmun)
    xcidade = _txt(end_ext, "xCidade")
    if xcidade:
        return xcidade
    return "-"


def _postal(end_nac, end_ext) -> str:
    cep = _txt(end_nac, "CEP")
    if cep:
        return fmt.cep(cep)
    return _txt(end_ext, "cEndPost")


def build_data(nfse: dict) -> dict:
    inf = _node(nfse, "infNFSe")
    dps = _node(inf, "DPS")
    inf_dps = _node(dps, "infDPS")
    prest = _node(inf_dps, "prest")
    reg_trib = _node(prest, "regTrib")
    emit = _node(inf, "emit")
    ender_emit = _node(emit, "enderNac")
    toma = _node(inf_dps, "toma")
    end_toma = _node(toma, "end")
    interm = _node(inf_dps, "interm")
    end_interm = _node(interm, "end")
    serv = _node(inf_dps, "serv")
    loc_prest = _node(serv, "locPrest")
    c_serv = _node(serv, "cServ")
    valores = _node(inf_dps, "valores")
    v_serv_prest = _node(valores, "vServPrest")
    trib = _node(valores, "trib")
    trib_mun = _node(trib, "tribMun")
    trib_fed = _node(trib, "tribFed")
    tot_trib = _node(trib, "totTrib")
    tot_trib_pct = _node(tot_trib, "pTotTrib")
    tot_trib_val = _node(tot_trib, "vTotTrib")
    valores_nfse = _node(inf, "valores")
    desc_cond_incond = _node(valores, "vDescCondIncond")

    # Grupos IBS/CBS e destinatário (podem não existir no leiaute atual).
    ibscbs = _node(inf, "IBSCBS")
    ibscbs_val = _node(ibscbs, "valores")
    tot_cibs = _node(ibscbs, "totCIBS")
    dps_ibscbs = _node(inf_dps, "IBSCBS")
    dest = _node(dps_ibscbs, "dest")
    end_dest = _node(dest, "end")
    imovel = _node(dps_ibscbs, "imovel")
    obra = _node(serv, "obra")
    atv_evento = _node(serv, "atvEvento")
    info_compl = _node(serv, "infoCompl")
    chave_subst = _txt(inf_dps, "subst", "chSubstda").strip()

    # Chave de acesso (remove o prefixo "NFS" do Id).
    id_nfse = _txt(inf, "@Id")
    chave = id_nfse[3:] if id_nfse.startswith("NFS") else id_nfse

    # Endereços.
    ender_emit_txt = _join_addr(
        _txt(ender_emit, "xLgr"), _txt(ender_emit, "nro"), _txt(ender_emit, "xBairro")
    )
    uf_emit = _txt(ender_emit, "UF")
    x_loc_emi = _txt(inf, "xLocEmi")
    municipio_emit = f"{x_loc_emi} / {uf_emit}" if x_loc_emi and uf_emit else ""
    emit_ibge_cep = _codigo_ibge_cep(
        _txt(ender_emit, "cMun"), fmt.cep(_txt(ender_emit, "CEP")) if _txt(ender_emit, "CEP") else ""
    )

    ender_toma_txt = _join_addr(
        _txt(end_toma, "xLgr"), _txt(end_toma, "nro"), _txt(end_toma, "xBairro")
    )
    toma_ibge_cep = _codigo_ibge_cep(
        _txt(end_toma, "endNac", "cMun"),
        _postal(_node(end_toma, "endNac"), _node(end_toma, "endExt")),
    )
    toma_municipio = _municipio(_node(end_toma, "endNac"), _node(end_toma, "endExt"))

    ender_interm_txt = _join_addr(
        _txt(end_interm, "xLgr"), _txt(end_interm, "nro"), _txt(end_interm, "xBairro")
    )
    interm_ibge_cep = _codigo_ibge_cep(
        _txt(end_interm, "endNac", "cMun"),
        _postal(_node(end_interm, "endNac"), _node(end_interm, "endExt")),
    )
    interm_municipio = _municipio(_node(end_interm, "endNac"), _node(end_interm, "endExt"))

    ender_dest_txt = _join_addr(
        _txt(end_dest, "xLgr"),
        _txt(end_dest, "nro"),
        _txt(end_dest, "xCpl"),
        _txt(end_dest, "xBairro"),
    )
    dest_ibge_cep = _codigo_ibge_cep(
        _txt(end_dest, "endNac", "cMun"),
        _postal(_node(end_dest, "endNac"), _node(end_dest, "endExt")),
    )
    dest_municipio = _municipio(_node(end_dest, "endNac"), _node(end_dest, "endExt"))

    # Totais aproximados dos tributos (Lei 12.741/2012).
    tot_trib_fed = _pct_or_currency(_txt(tot_trib_pct, "pTotTribFed"), _txt(tot_trib_val, "vTotTribFed"))
    tot_trib_est = _pct_or_currency(_txt(tot_trib_pct, "pTotTribEst"), _txt(tot_trib_val, "vTotTribEst"))
    tot_trib_mun = _pct_or_currency(_txt(tot_trib_pct, "pTotTribMun"), _txt(tot_trib_val, "vTotTribMun"))
    totais_aprox = ""
    if tot_trib_fed != "-" or tot_trib_est != "-" or tot_trib_mun != "-":
        totais_aprox = (
            "Totais Aproximados dos Tributos cfe. Lei nº 12.741/2012: "
            f"Federais: {tot_trib_fed}; Estaduais: {tot_trib_est}; Municipais: {tot_trib_mun};"
        )

    # Informações complementares (união dos campos, na ordem do leiaute).
    item_ped = _txt(info_compl, "gItemPed", "xItemPed")
    partes = [
        ("Inf. Cont.", _txt(info_compl, "xInfComp").strip()),
        ("NFS-e Subst.", chave_subst),
        ("Doc. Ref.", _txt(info_compl, "docRef").strip()),
        ("Cod. Obra", _txt(obra, "cObra").strip()),
        ("Insc. Imob.", _txt(imovel, "inscImobFisc").strip()),
        ("Cod. Evt.", _txt(atv_evento, "idAtvEvt").strip()),
        ("Doc. Tec.", _txt(info_compl, "idDocTec").strip()),
        ("Núm. Ped.", _txt(info_compl, "xPed").strip()),
        ("Item Ped.", item_ped.strip() if isinstance(item_ped, str) else ""),
        ("Inf. A. T. Mun.", _txt(inf, "xOutInf").strip()),
    ]
    info_complementares = fmt.limit(
        " | ".join(f"{label}: {valor}" for label, valor in partes if valor), 1997
    )

    c_trib_nac = _txt(c_serv, "cTribNac")
    c_trib_mun = _txt(c_serv, "cTribMun")
    x_trib_mun = _txt(inf, "xTribMun").strip()
    x_trib_nac = _txt(inf, "xTribNac").strip()
    c_loc_prest = _txt(loc_prest, "cLocPrestacao")

    data = {
        "chave_acesso": chave,
        "numero_nfse": _txt(inf, "nNFSe") or "-",
        "competencia": fmt.date(_txt(inf_dps, "dCompet")),
        "emissao_nfse": fmt.date_time(_txt(inf, "dhProc")),
        "numero_dps": _txt(inf_dps, "nDPS") or "-",
        "serie_dps": _txt(inf_dps, "serie") or "-",
        "emissao_dps": fmt.date_time(_txt(inf_dps, "dhEmi")),
        "ambiente": int(_txt(inf_dps, "tpAmb") or 1),
        "emitente_nfse": enums.emitente_nfse(_txt(inf_dps, "tpEmit")),
        "situacao": "NFS-e Emitida" if _txt(inf, "cStat") else "-",
        "finalidade": enums.finalidade(_txt(dps_ibscbs, "finNFSe")),
        "emitente": {
            "nome": _txt(emit, "xNome") or "-",
            "cnpj_cpf": fmt.cnpj_cpf(_doc(emit)),
            "im": "-",
            "telefone": fmt.phone(_txt(emit, "fone")),
            "email": _txt(emit, "email").lower(),
            "endereco": ender_emit_txt or "-",
            "municipio": municipio_emit or "-",
            "cep": emit_ibge_cep,
            "simples_nacional": enums.op_simp_nac(_txt(reg_trib, "opSimpNac")),
            "regime_sn": enums.reg_ap_trib_sn(_txt(reg_trib, "regApTribSN")),
        },
        "tomador": None
        if toma is None
        else {
            "nome": _txt(toma, "xNome") or "-",
            "cnpj_cpf": fmt.cnpj_cpf(_doc(toma)),
            "im": _txt(toma, "IM") or "-",
            "telefone": fmt.phone(_txt(toma, "fone")),
            "email": _txt(toma, "email").lower(),
            "endereco": ender_toma_txt or "-",
            "municipio": toma_municipio,
            "cep": toma_ibge_cep,
        },
        "intermediario": None
        if interm is None
        else {
            "nome": _txt(interm, "xNome") or "-",
            "cnpj_cpf": fmt.cnpj_cpf(_doc(interm)),
            "im": _txt(interm, "IMPrestMun") or "-",
            "telefone": fmt.phone(_txt(interm, "fone")),
            "email": _txt(interm, "email").lower(),
            "endereco": ender_interm_txt or "-",
            "municipio": interm_municipio,
            "cep": interm_ibge_cep,
        },
        "destinatario": None
        if dest is None
        else {
            "nome": _txt(dest, "xNome") or "-",
            "cnpj_cpf": fmt.cnpj_cpf(_doc(dest) or "-"),
            "telefone": fmt.phone(_txt(dest, "fone") or "-"),
            "email": _txt(dest, "email").lower() or "-",
            "endereco": ender_dest_txt or "-",
            "municipio": dest_municipio,
            "cep": dest_ibge_cep,
        },
        "servico": {
            "codigo_trib_nacional": fmt.cod_trib_nacional(c_trib_nac),
            "codigo_trib_municipal": c_trib_mun or "-",
            "codigo_trib_nac_mun": fmt.cod_trib_nac_mun(c_trib_nac, c_trib_mun),
            "codigo_nbs": _txt(c_serv, "cNBS") or "-",
            "desc_trib_nac_mun": x_trib_mun or x_trib_nac or "-",
            "local_prestacao_pais": (
                muni_lookup(c_loc_prest)
                if c_loc_prest
                else (_txt(loc_prest, "cPaisPrestacao") or _txt(inf, "xLocPrestacao") or "-")
            ),
            "descricao": _txt(c_serv, "xDescServ") or "-",
        },
        "tributacao_municipal": None
        if trib_mun is None
        else {
            "tributacao_issqn": enums.trib_issqn(_txt(trib_mun, "tribISSQN")),
            "municipio_incidencia": (
                muni_lookup(_txt(inf, "cLocIncid"))
                if _txt(inf, "cLocIncid")
                else (_txt(inf, "xLocIncid") or "-")
            ),
            "regime_especial": enums.reg_esp_trib(_txt(reg_trib, "regEspTrib")),
            "bc_issqn": (
                fmt.currency(_txt(trib_mun, "vBC"))
                if _present(_txt(trib_mun, "vBC"))
                else (fmt.currency(_txt(valores_nfse, "vBC")) if _present(_txt(valores_nfse, "vBC")) else "-")
            ),
            "aliquota": (
                f"{_txt(trib_mun, 'pAliq')}%"
                if _present(_txt(trib_mun, "pAliq"))
                else (f"{_txt(valores_nfse, 'pAliqAplic')}%" if _present(_txt(valores_nfse, "pAliqAplic")) else "-")
            ),
            "retencao_issqn": enums.tp_ret_issqn(_txt(trib_mun, "tpRetISSQN")),
            "issqn_apurado": (
                fmt.currency(_txt(trib_mun, "vISSQN"))
                if _present(_txt(trib_mun, "vISSQN"))
                else (fmt.currency(_txt(valores_nfse, "vISSQN")) if _present(_txt(valores_nfse, "vISSQN")) else "-")
            ),
        },
        "tributacao_federal": {
            "irrf": fmt.currency(_txt(trib_fed, "vRetIRRF")) if _present(_txt(trib_fed, "vRetIRRF")) else "-",
            "cp": fmt.currency(_txt(trib_fed, "vRetCP")) if _present(_txt(trib_fed, "vRetCP")) else "-",
            "contrib_sociais": fmt.currency(_txt(trib_fed, "vRetCSLL")) if _present(_txt(trib_fed, "vRetCSLL")) else "-",
            "desc_contrib_sociais": enums.tp_ret_pis_cofins(_txt(trib_fed, "piscofins", "tpRetPisCofins")),
            "pis": fmt.currency(_txt(trib_fed, "piscofins", "vPis")) if _present(_txt(trib_fed, "piscofins", "vPis")) else "-",
            "cofins": fmt.currency(_txt(trib_fed, "piscofins", "vCofins")) if _present(_txt(trib_fed, "piscofins", "vCofins")) else "-",
        },
        "totais": {
            "valor_servico": fmt.currency(_txt(v_serv_prest, "vServ")),
            "desconto_condicionado": (
                fmt.currency(_txt(trib_mun, "vDescCond") or _txt(desc_cond_incond, "vDescCond"))
                if _present(_txt(trib_mun, "vDescCond") or _txt(desc_cond_incond, "vDescCond"))
                else "-"
            ),
            "desconto_incondicionado": (
                fmt.currency(_txt(trib_mun, "vDescIncond") or _txt(desc_cond_incond, "vDescIncond"))
                if _present(_txt(trib_mun, "vDescIncond") or _txt(desc_cond_incond, "vDescIncond"))
                else "-"
            ),
            "total_retencoes": (
                fmt.currency(_txt(valores_nfse, "vTotalRet"))
                if _present(_txt(valores_nfse, "vTotalRet"))
                else _sum_currency(
                    _txt(trib_fed, "vRetIRRF"),
                    _txt(trib_fed, "vRetCP"),
                    _txt(trib_fed, "vRetCSLL"),
                )
            ),
            "valor_liquido": fmt.currency(_txt(valores_nfse, "vLiq")),
            "total_ibscbs": _sum_currency(
                _txt(tot_cibs, "gIBS", "vIBSTot"), _txt(tot_cibs, "gCBS", "vCBS")
            ),
            "valor_liquido_ibscbs": (
                fmt.currency(_txt(tot_cibs, "vTotNF"))
                if _present(_txt(tot_cibs, "vTotNF"))
                else fmt.currency(_txt(valores_nfse, "vLiq"))
            ),
        },
        "totais_aprox_tributos": totais_aprox,
        "municipio_emissao": (
            f"Município: {x_loc_emi}" + (f" / {uf_emit}" if uf_emit else "")
            if x_loc_emi and c_trib_nac != "99"
            else ""
        ),
        "ambiente_gerador": enums.amb_ger(_txt(inf, "ambGer")),
        "tipo_ambiente": enums.tp_amb(_txt(inf_dps, "tpAmb")),
        "tributacao_ibscbs": _build_ibscbs(ibscbs, ibscbs_val, tot_cibs, dps_ibscbs, valores_nfse, trib_fed, desc_cond_incond),
        "informacoes_complementares": info_complementares,
    }
    return data


def _build_ibscbs(ibscbs, ibscbs_val, tot_cibs, dps_ibscbs, valores_nfse, trib_fed, desc_cond_incond):
    if ibscbs is None:
        return None
    g_ibscbs = _node(_node(_node(dps_ibscbs, "valores"), "trib"), "gIBSCBS")
    uf = _node(ibscbs_val, "uf")
    mun = _node(ibscbs_val, "mun")
    fed = _node(ibscbs_val, "fed")
    g_ibs = _node(tot_cibs, "gIBS")
    g_cbs = _node(tot_cibs, "gCBS")

    def pct(node, key):
        v = _txt(node, key)
        return f"{v}%" if _present(v) else "-"

    def money(node, *path):
        v = _txt(node, *path)
        return fmt.currency(v) if _present(v) else "-"

    cod_incid = _txt(ibscbs, "cLocalidadeIncid")
    return {
        "cst": _txt(g_ibscbs, "CST"),
        "class_trib": _txt(g_ibscbs, "cClassTrib"),
        "ind_op": _txt(dps_ibscbs, "cIndOp"),
        "cod_ibge_incidencia": cod_incid,
        "municipio_incidencia_uf": muni_lookup(cod_incid) if cod_incid else _txt(ibscbs, "xLocalidadeIncid"),
        "exclusoes_reducoes": _sum_currency(
            _txt(desc_cond_incond, "vDescCond"),
            _txt(desc_cond_incond, "vDescIncond"),
            _txt(ibscbs_val, "vCalcReeRepRes"),
            _txt(valores_nfse, "vISSQN"),
            _txt(trib_fed, "piscofins", "vPis"),
            _txt(trib_fed, "piscofins", "vCofins"),
        ),
        "vbc": money(ibscbs_val, "vBC"),
        "p_red_aliq_uf": _txt(uf, "pRedAliqUF"),
        "p_red_aliq_mun": _txt(mun, "pRedAliqMun"),
        "p_red_aliq_cbs": _txt(fed, "pRedAliqCBS"),
        "p_ibs_uf": _txt(uf, "pIBSUF"),
        "p_ibs_mun": _txt(mun, "pIBSMun"),
        "p_aliq_efet_mun": pct(mun, "pAliqEfetMun"),
        "v_ibs_mun": money(g_ibs, "gIBSMunTot", "vIBSMun"),
        "p_aliq_efet_uf": pct(uf, "pAliqEfetUF"),
        "v_ibs_uf": money(g_ibs, "gIBSUFTot", "vIBSUF"),
        "v_ibs_tot": money(g_ibs, "vIBSTot"),
        "p_cbs": pct(fed, "pCBS"),
        "p_aliq_efet_cbs": pct(fed, "pAliqEfetCBS"),
        "v_cbs": money(g_cbs, "vCBS"),
    }
