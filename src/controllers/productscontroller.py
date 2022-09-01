from datetime import datetime
from bson.objectid import ObjectId
from flask_restx import Resource
from .namespaces import products
from flask import Flask, json, jsonify, Response, request
from dbmongo.mongoconnect import db
from models import product
from bson import json_util
from datetime import datetime, timedelta

@products.route('/create')
class create(Resource):
    def post(self):
        data: product = product().load(request.get_json())
        id =  db.products.insert(data)
        response = jsonify({'message':'Operación Completada', "id": str(id), "status_code": 200})
        return response#Response(response, mimetype='application/json')

@products.route('/update')
class update(Resource):
    def put(self):
        id:str=(request.json['_id'])['$oid']
        data: product = product().load(request.get_json(), unknown='INCLUDE')
        producttmp =  db.products.find_one_and_update({ '_id': ObjectId(id) } , { "$set": {
             'name': data['name'],
            'idregion': data['idregion'],
            'totalbuy': data['totalbuy'],
            'totalkgbuy': data['totalkgbuy'],
            'ingredients': data['ingredients'],
            'adicional': data['adicional']
            # 'inventario': data['inventario']
        }
        } )
        response = jsonify({'message':'Operación Completada', "id": str(id), "status_code": 200})
        return response#Response(response, mimetype='application/json')

@products.route('/getall')
class get_products(Resource):
    def get(self):
        products = db.products.find()
        return Response(json_util.dumps(products), mimetype='application/json')

@products.route('/get')
class get_products_by_name(Resource):
    @products.param('name', 'Nombre del producto', required=True)
    def get(selft):
        name:str= str(request.args['name'])
        query = { "$where": "this.name.toLowerCase().indexOf('"+name+"') >= 0" }
        products = db.products.find(query)
        response = json_util.dumps(products)
        return Response(response, mimetype='application/json')

@products.route('/provide')
class provide(Resource):
    def put(self):
        id:str=(request.json['_id'])['$oid']
        inventario:float = request.json['inventario']        
        TAG:str=request.json['TAG']
        productsUpt = db.products.find({ '_id': ObjectId(id) })
        productsUpt = json_util.dumps(productsUpt)
        productsUpt = json.loads(productsUpt)[0]
        newinventario = 0
        productionPrice:float= 0

        for item in productsUpt["ingredients"]:
            ingredientUpt = db.ingredients.find({ '_id': ObjectId(item["id"]) })
            ingredientUpt = json_util.dumps(ingredientUpt) 
            ingredientUpt = json.loads(ingredientUpt)[0]
            # productionPrice += (item["quantity"]*(item["price"]/float(item["kgContainer"])))
            if ingredientUpt["quantity"]-item["quantity"] < 0:
                response = jsonify({'message':'Inventario insuficiente '+ingredientUpt["name"], "id": str(id), "status_code": 400}) 
                return response
            # response = db.ingredients.find_one_and_update({ '_id': ObjectId(item["id"]) }, { "$set":{
            #     'quantity': ingredientUpt["quantity"]-item["quantity"]
            # }})


        for item in productsUpt["ingredients"]:
            ingredientUpt = db.ingredients.find({ '_id': ObjectId(item["id"]) })
            ingredientUpt = json_util.dumps(ingredientUpt) 
            ingredientUpt = json.loads(ingredientUpt)[0]
            productionPrice += (item["quantity"]*(item["price"]/float(item["kgContainer"])))
            response = db.ingredients.find_one_and_update({ '_id': ObjectId(item["id"]) }, { "$set":{
                'quantity': ingredientUpt["quantity"]-item["quantity"]
            }})
            
        for adicional in productsUpt["adicional"]:
                productionPrice += adicional['price']

        if not (productsUpt.get('inventario') is None):
            newinventario = productsUpt["inventario"]+inventario
        else:
            newinventario = inventario
            
        ingredient = db.products.find_one_and_update({ '_id': ObjectId(id) }, { "$set":{
            'inventario': newinventario
        }
        })
        id = db.provideProducts.insert({
            'reference':id,
            'TAG':TAG,
            'inventario': inventario,
            'created_at': datetime.now(),
            'production_price': productionPrice
        })
        response = jsonify({'message':'Ingrediente actualizado correctamente.', "id": str(id), "status_code": 200}) 
        return response

@products.route('/delete')
class delete(Resource):
    @products.param('id', 'object_id del producto a eliminar', required=True)
    def delete(self):
        id:str= str(request.args['id']) 
        db.products.find_one_and_delete({ '_id': ObjectId(id) })
        response = jsonify({'message':'Ingrediente elimnado correctamente.', "id": str(id), "status_code": 200}) 
        return response


@products.route('/gethistory')
class get_history(Resource):
    @products.param('toDate', 'Fecha Fin', required=True)
    @products.param('fromDate', 'Fecha Inicio', required=True)
    @products.param('id', required=True)
    def get(self):
        id:str= request.args['id']
        fromDate:datetime = request.args['fromDate']
        toDate:datetime = request.args['toDate']

        str_date = datetime.fromisoformat(toDate) + timedelta(seconds=86399)
        query = { "reference":id, "created_at": { "$gte": datetime.fromisoformat(fromDate), "$lt": str_date }}
        history = db.provideProducts.find(query)
        return  Response(json_util.dumps(history), mimetype='application/json')

@products.route('/getdatehistory')
class get_date_history(Resource):
    @products.param('toDate', 'Fecha Fin', required=True)
    @products.param('fromDate', 'Fecha Inicio', required=True)
    def get(self):
        fromDate:datetime = request.args['fromDate']
        toDate:datetime = request.args['toDate']

        str_date = datetime.fromisoformat(toDate) + timedelta(seconds=86399)
        query = { "created_at": { "$gte": datetime.fromisoformat(fromDate), "$lt": str_date }}
        # lookup = { "$lookup": { "from": "provide", "foreignField": "reference", "localField": "_id", "as": "provideIngredients"} }
        # print(lookup)
        history = json.loads(json_util.dumps(db.provideProducts.find(query)))
        products = json.loads(json_util.dumps(db.products.find()))
        for item in history:
            product = next((prod for prod in products if prod['_id']['$oid'] == item["reference"]), None)
            item["product"] = product


        # history = db.ingredients.aggregate({ "$addFields": { "_id": { "$toString": "$_id" }}},lookup)
        return  Response(json_util.dumps(history), mimetype='application/json')