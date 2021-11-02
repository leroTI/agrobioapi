from flask import Flask, jsonify, request
from flask.wrappers import Response
from flask_restx import Api, Resource
from flask_pymongo import PyMongo, ObjectId
from bson import json_util
from flask_cors import CORS
from bson.objectid import ObjectId
from controllers import connect, ingredientns,products
from dbmongo.mongoconnect import db


bioapp = Flask(__name__)
CORS(bioapp)
api = Api(
    bioapp,
    title='Bioapi Flask',
    doc='/docs',
    prefix='/api',
    version='1.0.0.0'
    )

api.add_namespace(connect)
api.add_namespace(ingredientns)
api.add_namespace(products)
# @api.route('/connect',methods=['GET'])
# class ping(Resource):
#     def connect(self):
#         return jsonify({"message":"pong!"})

# @bioapp.route("/ingredients/create", methods=['POST'])
# def create():
#     return ingredient.create(request.json['name'], request.json['kgContainer'], request.json['price'], 0)
    
# @bioapp.route("/ingredients/update", methods=['PUT'])
# def update():
#     _ingredient = ingredient.update((request.json['id'])['$oid'],request.json['name'], request.json['kgContainer'], request.json['price'])
#     if _ingredient:
#         response = jsonify({'message':'Ingrediente actualizado correctamente.', "id": str(request.json['id']), "status_code": 200}) 
#         return response
#     else:
#         return not_found()

# @bioapp.route("/ingredients/delete/<string:id>", methods=['DELETE'])
# def delete(id):    
#     _ingredient = ingredient.delete(id)
#     if _ingredient:
#         response = jsonify({'message':'Ingrediente elimnado correctamente.', "id": str(id), "status_code": 200}) 
#         return response
#     else:
#         return not_found()

# @bioapp.route('/ingredients/getall', methods=['GET'])
# def get_ingredients():
#     ingredients =  ingredient.get_ingredients()
#     return Response(ingredients, mimetype='application/json')

# @bioapp.route('/ingredients/get/<string:name>', methods=['GET'])
# def get_ingredients_by_name(name):
#     _ingredients = ingredient.get_ingredients_by_name(name)
#     response = json_util.dumps(_ingredients)
#     return Response(response, mimetype='application/json')

# @bioapp.route("/ingredients/provide", methods=['PUT'])
# def provide():
#     _ingredient = ingredient.provide((request.json['id'])['$oid'], request.json['price'], request.json['quantity'], request.json['TAG'] )
#     if _ingredient:
#         response = jsonify({'message':'Ingrediente actualizado correctamente.', "id": str(request.json['id']), "status_code": 200}) 
#         return response
#     else:
#         return not_found()

# @bioapp.route('/ingredients/gethistory/<string:id>/<string:fromDate>/<string:toDate>', methods=['GET'])
# def get_history(id, fromDate, toDate):
#     ingredients =  ingredient.get_history(id, fromDate, toDate)
#     print(ingredients)
#     return Response(ingredients, mimetype='application/json')


# @api.route('/ping')
# class Ping(Resource):
#     def get(self):
#         response = jsonify({"message":"pong!"})
#         response.status_code = 200
#         return response
            


###############################################
@bioapp.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message':'Resource Not Found: '+request.url,
        'status':404
    })
    response.status_code = 404
    return response
##################################################

if __name__ == '__main__':
    bioapp.run(debug = True, port=4000)