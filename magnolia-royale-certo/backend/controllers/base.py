from flask import jsonify, request, Response
from flask.views import MethodView
from backend.database import db
from backend.errors import AppError


def dados():
    value = request.get_json(silent=True)
    if not isinstance(value, dict):
        raise AppError('Envie um objeto JSON válido.')
    return value


class ApiController(MethodView):
    def dispatch_request(self, **kwargs):
        result = super().dispatch_request(**kwargs)
        db.session.commit()
        if isinstance(result, Response):
            return result
        return jsonify(result)
