"""Converte o XML da NFS-e Nacional em uma árvore de dicts aninhados.

Equivalente ao ``XmlToArray`` do projeto de referência, de forma defensiva e
agnóstica a namespace/prefixo: cada elemento vira um dict cujas chaves são os
nomes locais das tags; folhas viram strings; atributos entram com o prefixo
``@`` (ex.: ``@Id``); elementos repetidos viram listas.
"""
from __future__ import annotations

from lxml import etree

from .errors import XmlInvalidoError


def _localname(tag) -> str:
    if not isinstance(tag, str):
        return ""
    return tag.split("}", 1)[-1]


def _to_obj(el):
    children = [c for c in el if isinstance(c.tag, str)]  # ignora comentários/PIs
    if not children:
        text = (el.text or "").strip()
        if el.attrib:
            node = {f"@{_localname(k)}": v for k, v in el.attrib.items()}
            if text:
                node["#text"] = text
            return node
        return text

    node = {f"@{_localname(k)}": v for k, v in el.attrib.items()}
    for child in children:
        key = _localname(child.tag)
        value = _to_obj(child)
        if key in node:
            if not isinstance(node[key], list):
                node[key] = [node[key]]
            node[key].append(value)
        else:
            node[key] = value
    return node


def parse(xml) -> dict:
    """Devolve ``{"<raiz>": {...}}`` a partir do XML (str ou bytes)."""
    if isinstance(xml, str):
        xml = xml.encode("utf-8")
    if not isinstance(xml, (bytes, bytearray)):
        raise XmlInvalidoError("O XML deve ser uma str ou bytes.")
    parser = etree.XMLParser(resolve_entities=False, no_network=True, recover=False)
    try:
        root = etree.fromstring(xml, parser=parser)
    except etree.XMLSyntaxError as exc:
        raise XmlInvalidoError(f"XML malformado: {exc}") from exc
    return {_localname(root.tag): _to_obj(root)}
