from flask import Flask, jsonify, request, redirect
from flask.wrappers import Response
from flask_restx import Api, Resource
from flask_pymongo import PyMongo, ObjectId
from bson import json_util
from flask_cors import CORS
from bson.objectid import ObjectId
from controllers import connect, ingredientns,products,sale, client, sesion, bills
from dbmongo.mongoconnect import db
from models.bill import bill


app = Flask(__name__)
CORS(app)
api = Api(
    app,
    title='Bioapi Flask',
    doc='/docs',
    prefix='/api',
    version='1.0.0.0'
    )

api.add_namespace(connect)
api.add_namespace(ingredientns)
api.add_namespace(products)
api.add_namespace(sale)
api.add_namespace(sesion)
api.add_namespace(client)
api.add_namespace(bills)

@app.route('/')
def index():
    return redirect("http://127.0.0.1:5000/docs", code=302)

@app.route('/ping')
class Ping(Resource):
    def get(self):
        response = jsonify({"message":"pong!"})
        response.status_code = 200
        return response
            


###############################################
@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message':'Resource Not Found: '+request.url,
        'status':404
    })
    response.status_code = 404
    return response
##################################################

if __name__ == '__main__':
    app.run(host='0.0.0.0')