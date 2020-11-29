# -*- coding: utf-8 -*-

from urllib.parse import quote

from jinja2 import Environment
from jinja2.environment import Template
from jinja2.loaders import FileSystemLoader


ENVIRONMENT = Environment(
    loader=FileSystemLoader('readme/templates')
)

ENVIRONMENT.globals.update(
    format=format,
    quote=quote,
)

def get_template(name: str) -> Template:
    return ENVIRONMENT.get_template(name)
