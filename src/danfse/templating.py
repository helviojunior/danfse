"""Ambiente Jinja2 para o template da DANFSe."""
from __future__ import annotations

from functools import lru_cache

from jinja2 import Environment, PackageLoader, select_autoescape
from markupsafe import Markup, escape


def _nl2br(value) -> Markup:
    # Aceita tanto "\n" real quanto a sequência literal "\\n" (como no XML).
    text = str(value).replace("\\n", "\n")
    lines = escape(text).split("\n")
    return Markup("<br>\n".join(lines))


@lru_cache(maxsize=1)
def environment() -> Environment:
    env = Environment(
        loader=PackageLoader("danfse", "templates"),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["nl2br"] = _nl2br
    return env


def render(template_name: str, **context) -> str:
    return environment().get_template(template_name).render(**context)
