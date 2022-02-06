from datetime import datetime, timedelta
from dbmongo.mongoconnect import db
from .namespaces import sesion
from flask import Flask, json, jsonify, Response, request
from bson import json_util
from flask_restx import Resource
from bson.objectid import ObjectId

@sesion.route('/open')
class SesionOpen(Resource):
    def post(self):
        data = json.loads(json_util.dumps(request.json))
        id = db.sesion.insert(
            {
                '_id': str(ObjectId()),
                'create_at': datetime.now(),
                'closed_at': None,
                'starting_amount': request.json['starting_amount'],
                "sale_amount":None,
                "credit_amount":None,
                "closing_amount": None,
                'id_estatus':1
            }
        )

        response = jsonify({'message':'Operación Completada', "id": str(id), "status_code": 200})
        return response

@sesion.route('/sesionopen')
class get_sesion_open(Resource):
    def get(self):
        query = { "id_estatus": 1 }
        sesions = db.sesion.find(query)
        return  Response(json_util.dumps(sesions), mimetype='application/json')

@sesion.route('/sesiondaynow')
class get_sesion_open_day(Resource):
    @sesion.param('create_at', 'Fecha', required=True)
    def get(self):
        create_at : datetime = request.args['create_at']
        str_date = datetime.fromisoformat(create_at) + timedelta(seconds=86399)
        query = { "id_estatus": 1, "created_at": { "$gte": datetime.fromisoformat(create_at), "$lt": str_date } }
        sesions = db.sesion.find(query)
        return  Response(json_util.dumps(sesions), mimetype='application/json')

@sesion.route('/close')
class SesionClose(Resource):
    def put(self):
        id = db.sesion.find_one_and_update({ "_id": str((request.json['_id'])) }, {
            "$set":
            {
                'closed_at': datetime.now(),
                "sale_amount":request.json['sale_amount'],
                "credit_amount":request.json['credit_amount'],
                "closing_amount": request.json['closing_amount'],
                'id_estatus':2
            }
        }
        )

        response = jsonify({'message':'Operación Completada', "id": str(id), "status_code": 200})
        return response
