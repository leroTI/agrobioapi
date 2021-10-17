from flask_restplus import Resource, Namespace
import json
from datetime import datetime, timedelta
from flask import Flask, jsonify, Response
from flask_pymongo import PyMongo, ObjectId
from pymongo.message import query
from werkzeug.datastructures import ContentSecurityPolicy
from dbmongo.mongoconnect import db
from bson import json_util
from datetime import datetime

# ingredient = Namespace('ingredients') 

# class ingredient(Resource):
def create(name:str, kgContainer:float, price:float, quantity:float):
    id = db.ingredients.insert({
        'name':name,
        'kgContainer':kgContainer,
        'price':price,
        'quantity':quantity
    })
    response = jsonify({'message':'Operación Completada', "id": str(id), "status_code": 200})
    return response

def update(id:str,name:str, kgContainer:float, price:float):
    ingredient = db.ingredients.find_one_and_update({ '_id': ObjectId(id) }, { "$set":{
        'name':name,
        'kgContainer':kgContainer,
        'price':price
    }
    })
    return ingredient

def delete(id:str):
    return db.ingredients.find_one_and_delete({ '_id': ObjectId(id) })

def get_ingredients():
    ingredients = db.ingredients.find()
    return json_util.dumps(ingredients)

def get_ingredients_by_name(name):
    query = { "$where": "this.name.toLowerCase().indexOf('"+name+"') >= 0" }
    ingredients = db.ingredients.find(query)
    response = json_util.dumps(ingredients)
    return Response(response, mimetype='application/json')


def provide(id:str,  pricebuy:int, quantity:float, TAG:str):
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
    return ingredient

def get_history(id:str, fromDate:datetime, toDate:datetime):
    str_date = datetime.fromisoformat(toDate) + timedelta(seconds=86399)
    query = { "reference":id, "created_at": { "$gte": datetime.fromisoformat(fromDate), "$lt": str_date }}
    history = db.provide.find(query)
    return json_util.dumps(history)