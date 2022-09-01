from operator import ilshift, imod
from bson.objectid import ObjectId
from flask_restx import Resource
from flask import Flask, json, jsonify, Response, request
from dbmongo.mongoconnect import db
from bson import json_util
from datetime import datetime, timedelta

from .namespaces import bills
from models import bill
from bson import json_util

@bills.route('/create')
class create(Resource):
    def post(self):
        data:bill = bill().load(request.get_json())
        id =  db.bills.insert({
            '_id':str(ObjectId()),
            'name': data['name']
        })
        response = jsonify({'message':'Operación Completada', "id": str(id), "status_code": 200})
        return response#Response(response, mimetype='application/json')

@bills.route('/update')
class update(Resource):
    def put(self):
        id:str=(request.json['_id'])
        data: bill = bill().load(request.get_json(), unknown='INCLUDE')
        billsresult =  db.bills.find_one_and_update({ '_id': id } , { "$set": {
            'name': data['name']
        }
        } )
        response = jsonify({'message':'Operación Completada', "id": str(id), "status_code": 200})
        return response#Response(response, mimetype='application/json')


@bills.route('/delete')
class delete(Resource):
    @bills.param('id', 'object_id del gasto a eliminar', required=True)
    def delete(self):
        id:str= str(request.args['id']) 
        db.bills.find_one_and_delete({ '_id': ObjectId(id) })
        response = jsonify({'message':'Ingrediente elimnado correctamente.', "id": str(id), "status_code": 200}) 
        return response



@bills.route('/getall')
class get_bills(Resource):
    def get(self):
        bills = db.bills.find()
        return Response(json_util.dumps(bills), mimetype='application/json')