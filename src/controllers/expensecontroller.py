from .namespaces import expenses
from flask_restx import Resource
from models import expense
from flask import json,jsonify, Response, request
from dbmongo.mongoconnect import db
from bson import ObjectId, json_util
from datetime import datetime, timedelta

@expenses.route('/pay')
class pay(Resource):
    def post(self):
        data = json.loads(json_util.dumps(request.json))
        id = db.expenses.insert({
            '_id': str(ObjectId()),
            'created_at': datetime.now(),
            'clave': data['clave'],
            'import': data['import'],
            'expenses':data['expenses']
        })
        response = jsonify({'message':'Operación Completada', "id": str(id), "status_code": 200})
        return response#Response(response, mimetype='application/json')

@expenses.route('/gethistory')
class get_all(Resource):
    @expenses.param('to_date', 'Fecha Fin', required=True)
    @expenses.param('from_date', 'Fecha Inicio', required=True)
    def get(self):
        fromDate:datetime = request.args['from_date']
        toDate:datetime = request.args['to_date']

        str_date = datetime.fromisoformat(toDate) + timedelta(seconds=86399)
        query = { "created_at": { "$gte": datetime.fromisoformat(fromDate), "$lt": str_date }}
        expensesList = db.expenses.find(query)
        return  Response(json_util.dumps(expensesList), mimetype='application/json')

@expenses.route('/getexpensebyname')
class get_expenses_by_name(Resource):
    @expenses.param('name', 'Nombre del producto', required=True)
    @expenses.param('to_date', 'Fecha Fin', required=True)
    @expenses.param('from_date', 'Fecha Inicio', required=True)
    def get(selft):
        name:str= str(request.args['name'])
        fromDate:datetime = request.args['from_date']
        toDate:datetime = request.args['to_date']
        query = { "expenses": { "$elemMatch": { "name":name }} }
        expense = db.expenses.find(query)
        response = json_util.dumps(expense)
        return Response(response, mimetype='application/json')
