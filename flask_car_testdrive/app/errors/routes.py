from flask import render_template, jsonify

from app import db
from app.user import menu
from app.api.errors import ApiError
from app.errors import bp
from app.user.errors import HtmlError


# здесь ловятся все необработанные ошибки
# не могу настроить определение от апи другого приложения или от веба запрос
@bp.app_errorhandler(403)
def not_found_error(error):
    return render_template('errors/errors.html', main_menu=menu, title='Forbidden 403',
                           error=error), 403


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/errors.html', main_menu=menu, title='not_found_error 404',
                           error=error), 404


@bp.app_errorhandler(500)
def not_found_error(error):
    return render_template('errors/errors.html', main_menu=menu, title='internal_server_error 500',
                           error=error), 500


# здесь ловятся обработанные ошибки
# для взаимодействия с frontend все равно придется json с данными возвращать
@bp.app_errorhandler(HtmlError)
def handler_html_error(error):
    if len(error.args) == 2:
        response = {
            'error_place': error.error_place,
            'error_type': error.error_type,
            'error_description': error.args[0],
            'status_code': error.args[1]
        }
    else:
        response = {
            'error_place': error.error_place,
            'error_type': error.error_type,
            'error_description': error.args[0],
            'error_exception': error.args[1],
            'status_code': error.args[2]
        }

    db.session.rollback()
    return render_template('errors/handled_errors.html', main_menu=menu, response=response, title='error', )


@bp.app_errorhandler(ApiError)
def handler_api_error(error):
    if len(error.args) == 2:
        response = {
            'error_place': error.error_place,
            'error_type': error.error_type,
            'error_description': error.args[0]}

        db.session.rollback()
        return jsonify(response), error.args[1]

    else:
        response = {
            'error_place': error.error_place,
            'error_type': error.error_type,
            'error_description': error.args[0],
            'error_exception': error.args[1]
        }

    db.session.rollback()
    return jsonify(response), error.args[2]
