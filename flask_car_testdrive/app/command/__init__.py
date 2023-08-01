from flask import Blueprint

bp = Blueprint('command', __name__, template_folder='templates', static_folder='static')

from app.command import routes
