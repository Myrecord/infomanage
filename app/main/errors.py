from flask import render_template
from . import main


@main.app_errorhandler(404)
def not_found(e):
    return render_template('404.html')

@main.app_errorhandler(500)
def server_error(e):
    return render_temlpalte('500.html')
