import werkzeug

from app.errors import bp


# need test

@bp.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return 'bad request! 400', 400


@bp.errorhandler(404)
def handle_bad_request(error):
    return 'bad request! 404', 404
