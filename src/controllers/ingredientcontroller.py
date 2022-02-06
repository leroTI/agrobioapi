from cgitb import lookup
from flask_restx import Resource, Namespace
import json
from datetime import datetime, timedelta
from flask import Flask, jsonify, Response, request
from flask_pymongo import PyMongo, ObjectId
from pymongo.message import query
from werkzeug.datastructures import ContentSecurityPolicy
from dbmongo.mongoconnect import db
from bson import json_util
from .namespaces import ingredientns

@ingredientns.route('/create')
class create(Resource):
    def post(self):
        name:str = request.json['name']
        kgContainer:float = request.json['kgContainer']
        price:float=request.json['price']
        quantity:float = 0
        id = db.ingredients.insert({
            'name':name,
            'kgContainer':kgContainer,
            'price':price,
            'quantity':quantity
        })
        response = jsonify({'message':'Operación Completada', "id": str(id), "status_code": 200})
        return response#Response(response, mimetype='application/json')

@ingredientns.route('/update')
class update(Resource):
    def put(self):
        id:str=(request.json['id'])['$oid']
        name:str = request.json['name']
        kgContainer:float = request.json['kgContainer']
        price:float=request.json['price']

        ingredient = db.ingredients.find_one_and_update({ '_id': ObjectId(id) }, { "$set":{
            'name':name,
            'kgContainer':kgContainer,
            'price':price
        }
        })
        response = jsonify({'message':'Ingrediente actualizado correctamente.', "id": str(request.json['id']), "status_code": 200}) 
        return response

@ingredientns.route('/delete')
class delete(Resource):
    @ingredientns.param('id', 'object_id del ingrediente a eliminar', required=True)
    def delete(self):
        id:str= str(request.args['id']) 
        db.ingredients.find_one_and_delete({ '_id': ObjectId(id) })
        response = jsonify({'message':'Ingrediente elimnado correctamente.', "id": str(id), "status_code": 200}) 
        return response

@ingredientns.route('/getall')
class get_ingredients(Resource):
    def get(self):
        ingredients = db.ingredients.find()
        return Response(json_util.dumps(ingredients), mimetype='application/json')

@ingredientns.route('/get')
class get_ingredients_by_name(Resource):
    @ingredientns.param('name', 'Nombre del ingrediente', required=True)
    def get(selft):
        name:str= str(request.args['name'])
        query = { "$where": "this.name.toLowerCase().indexOf('"+name+"') >= 0" }
        ingredients = db.ingredients.find(query)
        response = json_util.dumps(ingredients)
        return Response(response, mimetype='application/json')

@ingredientns.route('/provide')
class provide(Resource):
    def put(self):
        id:str=(request.json['id'])['$oid']
        pricebuy:float = request.json['price']
        quantity:float=request.json['quantity']
        TAG:str=request.json['TAG']
        ingredientUpt = db.ingredients.find({ '_id': ObjectId(id) })
        ingredientUpt = json_util.dumps(ingredientUpt)    
        newquantity = json.loads(ingredientUpt)[0]["quantity"]+quantity
        ingredient = db.ingredients.find_one_and_update({ '_id': ObjectId(id) }, { "$set":{
            'price':pricebuy,
            'quantity': newquantity
        }
        })
        id = db.provide.insert({
            'reference':id,
            'TAG':TAG,
            'price':pricebuy,
            'quantity':quantity,
            'created_at':datetime.now()
        })
        response = jsonify({'message':'Ingrediente actualizado correctamente.', "id": str(request.json['id']), "status_code": 200}) 
        return response

@ingredientns.route('/gethistory')
class get_history(Resource):
    @ingredientns.param('toDate', 'Fecha Fin', required=True)
    @ingredientns.param('fromDate', 'Fecha Inicio', required=True)
    @ingredientns.param('id', required=True)
    def get(self):
        id:str= request.args['id']
        fromDate:datetime = request.args['fromDate']
        toDate:datetime = request.args['toDate']

        str_date = datetime.fromisoformat(toDate) + timedelta(seconds=86399)
        query = { "reference":id, "created_at": { "$gte": datetime.fromisoformat(fromDate), "$lt": str_date }}
        history = db.provide.find(query)
        return  Response(json_util.dumps(history), mimetype='application/json')

@ingredientns.route('/getdatehistory')
class get_date_history(Resource):
    @ingredientns.param('toDate', 'Fecha Fin', required=True)
    @ingredientns.param('fromDate', 'Fecha Inicio', required=True)
    def get(self):
        fromDate:datetime = request.args['fromDate']
        toDate:datetime = request.args['toDate']

        str_date = datetime.fromisoformat(toDate) + timedelta(seconds=86399)
        query = { "created_at": { "$gte": datetime.fromisoformat(fromDate), "$lt": str_date }}
        # lookup = { "$lookup": { "from": "provide", "foreignField": "reference", "localField": "_id", "as": "provideIngredients"} }
        # print(lookup)
        history = json.loads(json_util.dumps(db.provide.find(query)))
        ingredients = json.loads(json_util.dumps(db.ingredients.find()))
        for item in history:
            ingredient = next((ing for ing in ingredients if ing['_id']['$oid'] == item["reference"]), None)
            item["ingredient"] = ingredient
            print(ingredient)



        # history = db.ingredients.aggregate({ "$addFields": { "_id": { "$toString": "$_id" }}},lookup)
        return  Response(json_util.dumps(history), mimetype='application/json')