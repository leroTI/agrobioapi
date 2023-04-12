from datetime import datetime, timedelta
from tokenize import Number
from bson import json_util
from models.sell import sell
from .namespaces import sale
from flask_restx import Resource
from flask import Flask, json, jsonify, Response, request
from dbmongo.mongoconnect import db
from bson.objectid import ObjectId

@sale.route('/sell')
class sellPoint(Resource):
    def post(self):        
        data = json.loads(json_util.dumps(request.json))
        id = True
        for item in request.json['sale_products']:
            product = db.products.find({ '_id': ObjectId(item['id']) })
            product = json_util.dumps(product)
            product = json.loads(product)[0]
            if (product['inventario'] - item['cantidad']) < 0:
                mensaje = 'El producto '+product['name']+ ' no cuenta con el inventario suficiente'
                response = jsonify({'message':mensaje, "id": str(item['id']), "status_code": 400})
                return response


        if 'client' not in data:
            client = None
        else:
            client = data["client"]

        id =  db.sale.insert(
            {
            'cash':request.json['cash'],
            'payment': request.json['payment'],
            'credit': request.json['credit'],
            'total':request.json['total'],
            'cashback':request.json['cashback'],
            'id_region': request.json['id_region'],
            'id_sesion': request.json['id_sesion'],
            'client': client,
            'created_at':datetime.now(),
            'sale_products':  request.json['sale_products'],
            'outstanding_amount': float(request.json['total'])-float(request.json['payment']),
            'status': "open"
        })

        for item in request.json['sale_products']:
            product = db.products.find({ '_id': ObjectId(item['id']) })
            product = json_util.dumps(product)
            product = json.loads(product)[0]
            result = db.products.find_one_and_update({ '_id': ObjectId(item['id']) }, { "$set":{
            'inventario': product['inventario'] - item['cantidad']}})


        response = jsonify({'message':'Operación Completada', "id": str(id), "status_code": 200})
        return response#Response(response, mimetype='application/json')

@sale.route('/payment')
class payment(Resource):
    def post(self):        
        data = json.loads(json_util.dumps(request.json))      
        id =  db.payment.insert(
            {
            '_id': str(ObjectId()),
            'id_client':request.json['id_client'],
            'cash': request.json['cash'],
            'amount': request.json['amount'],
            'cashback':request.json['cashback'],
            'total':request.json['total'],
            'total_sales': request.json['total_sales'],
            'id_sesion': request.json['id_sesion'],
            'payment_at':datetime.now(),
            'status': "open"
        })
        amount = request.json['amount']

        query = { "client.id": request.json['id_client'] , "status": "open"}
        salesOpen = db.sale.find(query)
        salesOpen = json_util.dumps(salesOpen)
        salesOpen = json.loads(salesOpen)
        for item in salesOpen:
            if amount == 0:
                break
            status = item["status"]
            newOutstandingAmount = item["outstanding_amount"]
            if newOutstandingAmount>=amount:
                newOutstandingAmount = newOutstandingAmount - amount
                amount = 0.00
            else:
                amount = amount - newOutstandingAmount
                newOutstandingAmount = 0.00 
                        
            if newOutstandingAmount == 0.00:
                status = "closed"
            response = db.sale.find_one_and_update({ '_id': ObjectId(item["_id"]["$oid"]) }, { "$set" : { 'outstanding_amount': newOutstandingAmount, "status": status } })


        response = jsonify({'message':'Operación Completada', "id": str(id), "status_code": 200})
        return response#Response(response, mimetype='application/json')

@sale.route('/gethistoryregion')
class get_history_region(Resource):
    @sale.param('to_Date', 'Fecha Fin', required=True)
    @sale.param('from_Date', 'Fecha Inicio', required=True)
    @sale.param('id_region', required=True)
    def get(self):
        id:int=  request.args['id_region']
        fromDate:datetime = request.args['from_Date']
        toDate:datetime = request.args['to_Date']

        str_date = datetime.fromisoformat(toDate) + timedelta(seconds=86399)
        if (id == '0'):
            query = { "created_at": { "$gte": datetime.fromisoformat(fromDate), "$lt": str_date }}
        else:    
            query = { "id_region": int(id), "created_at": { "$gte": datetime.fromisoformat(fromDate), "$lt": str_date }}
        
        history = db.sale.find(query)
        return  Response(json_util.dumps(history), mimetype='application/json')

@sale.route('/gethistoryclient')
class get_history_client(Resource):
    @sale.param('to_date', 'Fecha Fin', required=True)
    @sale.param('from_date', 'Fecha Inicio', required=True)
    @sale.param('id_client', required=True)
    def get(self):
        id:str= request.args['id_client']
        fromDate:datetime = request.args['from_date']
        toDate:datetime = request.args['to_date']

        str_date = datetime.fromisoformat(toDate) + timedelta(seconds=86399)
        query = { "client.id": id , "created_at": { "$gte": datetime.fromisoformat(fromDate), "$lt": str_date }}
        sales = db.sale.find(query)

        query = { "id_client": id , "payment_at": { "$gte": datetime.fromisoformat(fromDate), "$lt": str_date }}
        payments = db.payment.find(query)

        history = {
            "sales": sales,
            "payments": payments
        }
        return  Response(json_util.dumps(history), mimetype='application/json')


@sale.route('/getsalesopenbyclient')
class get_sale_open_by_client(Resource):
    @sale.param('id_client', required=True)
    def get(self):
        id:str= request.args['id_client']
        query = { "client.id": id , "status": "open"}
        history = db.sale.find(query)
        return  Response(json_util.dumps(history), mimetype='application/json')

@sale.route('/gethistorysesion')
class get_history_sesion(Resource):
    @sale.param('id_sesion', required=True)
    def get(self):
        id:str=  request.args['id_sesion']
        query = { "id_sesion": str(id) }        
        history = db.sale.find(query)
        return  Response(json_util.dumps(history), mimetype='application/json')