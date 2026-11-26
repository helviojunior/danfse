"""Formatadores para padrões brasileiros (CNPJ, CPF, telefone, CEP, moeda, datas).

Port de ``src/Danfse/Formatter.php`` (guilhermecfviana/danfse-nacional, MIT).
"""
from __future__ import annotations

import re
from datetime import datetime

_NON_DIGIT = re.compile(r"\D")


def _digits(value: str) -> str:
    return _NON_DIGIT.sub("", value or "")


def cnpj_cpf(value: str) -> str:
    raw = (value or "").strip()
    if raw in ("", "-"):
        return "-"
    digits = _digits(raw)
    if len(digits) == 14:
        return f"{digits[0:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:14]}"
    if len(digits) == 11:
        return f"{digits[0:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:11]}"
    # NIF e demais documentos fora do padrão CPF/CNPJ: preserva o valor recebido.
    return value


def phone(value: str) -> str:
    if value in ("", "-") or value is None:
        return "-"
    digits = _digits(value)
    if len(digits) == 11:
        return f"({digits[0:2]}) {digits[2:7]}-{digits[7:11]}"
    if len(digits) == 10:
        return f"({digits[0:2]}) {digits[2:6]}-{digits[6:10]}"
    return value


def cep(value: str) -> str:
    if value in ("", "-") or value is None:
        return "-"
    digits = _digits(value)
    if len(digits) == 8:
        return f"{digits[0:5]}-{digits[5:8]}"
    return value


def _parse_dt(value: str):
    v = (value or "").strip()
    try:
        return datetime.fromisoformat(v)
    except ValueError:
        # Tolera 'Z' (UTC) e datas puras.
        try:
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        except ValueError:
            return None


def date(value: str) -> str:
    if value in ("", "-") or value is None:
        return "-"
    dt = _parse_dt(value)
    return dt.strftime("%d/%m/%Y") if dt else value


def date_time(value: str) -> str:
    if value in ("", "-") or value is None:
        return "-"
    dt = _parse_dt(value)
    return dt.strftime("%d/%m/%Y %H:%M:%S") if dt else value


def currency(value) -> str:
    if value in ("", "-", None):
        return "-"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "-"
    # number_format(x, 2, ',', '.')
    inteiro, _, decimal = f"{number:,.2f}".partition(".")
    inteiro = inteiro.replace(",", ".")
    return f"R$ {inteiro},{decimal}"


def cod_trib_nacional(value: str) -> str:
    if value in ("", "-") or value is None:
        return "-"
    digits = _digits(value)
    if len(digits) == 6:
        return f"{digits[0:2]}.{digits[2:4]}.{digits[4:6]}"
    return value


def cod_trib_nac_mun(nacional: str, municipal: str) -> str:
    nac = cod_trib_nacional(nacional)
    mun = (municipal or "").strip()
    if mun in ("", "-"):
        return nac
    if nac in ("", "-"):
        return mun
    return f"{nac} / {mun}"


def limit(value: str, max_len: int, end: str = "...") -> str:
    value = value or ""
    if len(value) <= max_len:
        return value
    return value[:max_len] + end
