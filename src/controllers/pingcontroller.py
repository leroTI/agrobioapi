from flask import jsonify
from flask_restx import Resource
from .namespaces import connect
from werkzeug.exceptions import HTTPException, InternalServerError


@connect.route('/ping2')
class ping2(Resource):
    def get(self):
        response = jsonify({"message":"pong!"})
        response.status_code = 200
        return response
