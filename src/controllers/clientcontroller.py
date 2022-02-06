from datetime import datetime

from bson import json_util
from bson.objectid import ObjectId
from models.sell import sell
from .namespaces import client
from flask_restx import Resource
from flask import Flask, json, jsonify, Response, request
from dbmongo.mongoconnect import db

@client.route('/create')
class create(Resource):
    def post(self):
        id =  db.cliente.insert(
            {
            'primerNombre': request.json['primerNombre'],
            'segundoNombre': request.json['segundoNombre'],
            'apellidos': request.json['apellidos'],
            'nombreCompleto': request.json['primerNombre']+" "+request.json['segundoNombre']+" "+request.json['apellidos'],
            # 'fechaNacimiento':request.json['fechaNacimiento'],
            'rfc':request.json['rfc'],
            'correo': request.json['correo'],
            'telefono': request.json['telefono'],
            'domicilio':  request.json['domicilio'],
            'idRegion': request.json['idRegion']
        })

        response = jsonify({'message':'Operación Completada', "id": str(id), "status_code": 200})
        return response

@client.route('/update')
class update(Resource):
    def put(self):
        id:str=(request.json['_id'])['$oid']
        id =  db.cliente.find_one_and_update({ '_id': ObjectId(id) },
        {
            "$set":
            {
            'primerNombre': request.json['primerNombre'],
            'segundoNombre': request.json['segundoNombre'],
            'apellidos': request.json['apellidos'],
            'nombreCompleto': request.json['primerNombre']+" "+request.json['segundoNombre']+" "+request.json['apellidos'],
            'rfc':request.json['rfc'],
            'correo': request.json['correo'],
            'telefono': request.json['telefono'],
            'domicilio':  request.json['domicilio'],
            'idRegion': request.json['idRegion']
        }
        })

        response = jsonify({'message':'Operación Completada', "id": str(id), "status_code": 200})
        return response

@client.route('/delete')
class delete(Resource):
    @client.param('id', 'object_id del cliente a eliminar', required=True)
    def delete(self):
        id:str= str(request.args['id']) 
        db.cliente.find_one_and_delete({ '_id': ObjectId(id) })
        response = jsonify({'message':'Cliente elimnado correctamente.', "id": str(id), "status_code": 200}) 
        return response


@client.route('/getall')
class get_clientes(Resource):
    def get(self):
        clients = db.cliente.find()
        return Response(json_util.dumps(clients), mimetype='application/json')

@client.route('/get')
class get_clientes_by_name(Resource):
    @client.param('name', 'Nombre del cliente', required=True)
    def get(selft):
        name:str= str(request.args['name'])
        query = { "$where": "this.nombreCompleto.toLowerCase().indexOf('"+name+"') >= 0" }
        cliente = db.cliente.find(query)
        response = json_util.dumps(cliente)
        return Response(response, mimetype='application/json')