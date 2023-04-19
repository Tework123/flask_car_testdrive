from flask import Blueprint
from app.admin import bp


@bp.route('/')
def index():
    return 'admin login'

