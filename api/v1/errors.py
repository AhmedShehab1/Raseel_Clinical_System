from werkzeug.http import HTTP_STATUS_CODES
from api.v1.views import bp
from werkzeug.exceptions import HTTPException


def error_response(status_code, message=None):
    data = {"error": HTTP_STATUS_CODES.get(status_code, "Unkown Error")}
    if message:
        data["message"] = message
    return data, status_code


@bp.errorhandler(HTTPException)
def handle_exception(error):
    return error_response(error.code)


def bad_request(message):
    return error_response(400, message=message)
