import os
import click
from flask import Blueprint

bp = Blueprint('cli', __name__, cli_group=None)

@bp.cli.group()
def translate():
    """Translation and Localization Commands"""
    pass

@translate.command()
def update():
    """Update all languages"""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError("extract command failed")
    if os.system('pybabel update -i messages.pot -d web_flask/translations'):
        raise RuntimeError("update command failed")
    os.remove('messages.pot')

@translate.command()
def compile():
    """Compile all languages"""
    if os.system('pybabel compile -d web_flask/translations'):
        raise RuntimeError("compile command failed")

@translate.command()
@click.argument('lang')
def init(lang):
    """Initialize a new language"""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError("extract command failed")
    if os.system('pybabel init -i messages.pot -d web_flask/translations -l ' + lang):
        raise RuntimeError('init Command failed')
    os.remove('messages.pot')
