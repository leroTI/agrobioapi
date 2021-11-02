from flask_restx import Resource
from .namespaces import products
from flask import Flask, jsonify, Response, request
from dbmongo.mongoconnect import db
from models import product

@products.route('/create')
class create(Resource):
    def post(self):
        data: product = product().load(request.get_json())
        print(data)
        id =  db.products.insert(data)
        response = jsonify({'message':'Operación Completada', "id": str(id), "status_code": 200})
        return Response(response, mimetype='application/json')