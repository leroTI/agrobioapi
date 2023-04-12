from operator import ilshift, imod
from bson.objectid import ObjectId
from flask_restx import Resource
from flask import Flask, json, jsonify, Response, request
from dbmongo.mongoconnect import db
from bson import json_util
from datetime import datetime, timedelta

from .namespaces import bills
from models import bill, capitalNeto
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


@bills.route('/get')
class get_bills_by_name(Resource):
    @bills.param('name', 'Nombre del gasto', required=True)
    def get(selft):
        name:str= str(request.args['name'])
        query = { "$where": "this.name.toLowerCase().indexOf('"+name+"') >= 0" }
        bills = db.bills.find(query)
        response = json_util.dumps(bills)
        return Response(response, mimetype='application/json')

@bills.route('/capital-neto')
class CreateCapitalNeto(Resource):
    def post(self):
        # data:capitalNeto = capitalNeto().load(request.get_json())
        #capital anterior
        pay = 0.00
        paymentSale = 0.00 
        credits = 0.00
        expensesSum = 0.00
        lista = db.capitalNeto.find().limit(1).sort("created_at", -1)
        if (lista != None):
            fromDate:datetime = str(lista[0]['created_at'])
            toDate:datetime = str(datetime.now())

            star_date = datetime.fromisoformat(fromDate) + timedelta(seconds=0)
            end_date = datetime.fromisoformat(toDate) + timedelta(seconds=0)
            print(star_date)
            print(end_date)
            query = { "created_at": { "$gte": star_date, "$lt": end_date }}
            expensesList = db.expenses.find(query)
        
            for item in expensesList:
                expensesSum += item["import"]
            
            historySale = db.sale.find(query)
            for sale in historySale:
                paymentSale += sale["payment"]
                credits += sale["credit"]

            query = { "payment_at": { "$gte": star_date, "$lt": end_date }}
            payments = db.payment.find(query)
            
            for paymentItem in payments:
                pay += paymentItem["amount"]

            query = {"status": "open"}
            totalCreditBalance = 0.00
            saleCreditBalance = db.sale.find(query)
            for creditsSale in saleCreditBalance:
                totalCreditBalance += creditsSale["outstanding_amount"]

            #Actualizar capital anterior
            result =  db.capitalNeto.find_one_and_update({ '_id': lista[0]["_id"] } , 
            { "$set": {
                  'expenses': expensesSum
                , 'paymentsSale': paymentSale
                , 'credits': credits
                , 'payments': pay
                , 'creditBalance': totalCreditBalance
                }
            } )

         

        id =  db.capitalNeto.insert({
            '_id':str(ObjectId()),
            'description': request.json['description'],
            'capital': request.json['capital'],
            'created_at':datetime.now(),
            'expenses': 0, 
            'paymentsSale': 0, 
            'credits': 0, 
            'payments': 0,
            'creditBalance': 0,
            'capitalBefore': (request.json['capital']+paymentSale+pay) -(expensesSum+credits)
        })
        response = jsonify({'message':'Operación Completada', "id": str(id), "status_code": 200})

        # response = jsonify({'_id': lista[0]["_id"]
        #                     , 'description': lista[0]["description"]
        #                     , 'capital': lista[0]["capital"]
        #                     , 'capitalBefore': lista[0]["capitalBefore"]
        #                     , 'created_at': lista[0]["created_at"]
        #                     , 'expenses': expensesSum
        #                     , 'paymentsSale': paymentSale
        #                     , 'credits': credits
        #                     , 'payments': pay
        #                     , 'creditBalance': totalCreditBalance
        #                     })
        return response#Response(response, mimetype='application/json')

@bills.route('/capital-neto')
class getCapitalNeto(Resource):
    def get(self):
        
        lista = db.capitalNeto.find().sort("created_at", -1)
        fromDate:datetime = str(lista[0]['created_at'])
        toDate:datetime = str(datetime.now())
        lista = json.loads(json_util.dumps(lista))

        print(fromDate)
        star_date = datetime.fromisoformat(fromDate) + timedelta(seconds=0)
        end_date = datetime.fromisoformat(toDate) + timedelta(seconds=0)
        print(star_date)
        print(end_date)
        query = { "created_at": { "$gte": star_date, "$lt": end_date }}
        expensesList = db.expenses.find(query)

        
        expensesSum = 0.00
        for item in expensesList:
            expensesSum += item["import"]

        paymentSale = 0.00 
        credits = 0.00
        historySale = db.sale.find(query)
        for sale in historySale:
            paymentSale += sale["payment"]
            credits += sale["credit"]

        query = { "payment_at": { "$gte": star_date, "$lt": end_date }}
        payments = db.payment.find(query)
        pay = 0.00
        for paymentItem in payments:
            pay += paymentItem["amount"]

        query = {"status": "open"}
        totalCreditBalance = 0.00
        saleCreditBalance = db.sale.find(query)
        for creditsSale in saleCreditBalance:
            totalCreditBalance += creditsSale["outstanding_amount"] 
        
        lista[0]["expenses"] = expensesSum
        lista[0]["paymentsSale"] = paymentSale
        lista[0]["credits"] = credits
        lista[0]["payments"] =  pay
        lista[0]["creditBalance"] = totalCreditBalance
        
        return  Response(json_util.dumps(lista), mimetype='application/json')
        # return Response(lista, mimetype='application/json')
    
@bills.route('/capital-neto/today')
class getCapitalNeto(Resource):
    def get(self):
        lista = db.capitalNeto.find().limit(1).sort("created_at", -1)

        fromDate:datetime = str(lista[0]['created_at'])
        toDate:datetime = str(datetime.now())

        print(fromDate)
        star_date = datetime.fromisoformat(fromDate) + timedelta(seconds=0)
        end_date = datetime.fromisoformat(toDate) + timedelta(seconds=0)
        print(star_date)
        print(end_date)
        query = { "created_at": { "$gte": star_date, "$lt": end_date }}
        expensesList = db.expenses.find(query)

        
        expensesSum = 0.00
        for item in expensesList:
            expensesSum += item["import"]

        paymentSale = 0.00 
        credits = 0.00
        historySale = db.sale.find(query)
        for sale in historySale:
            paymentSale += sale["payment"]
            credits += sale["credit"]

        query = { "payment_at": { "$gte": star_date, "$lt": end_date }}
        payments = db.payment.find(query)
        pay = 0.00
        for paymentItem in payments:
            pay += paymentItem["amount"]

        query = {"status": "open"}
        totalCreditBalance = 0.00
        saleCreditBalance = db.sale.find(query)
        for creditsSale in saleCreditBalance:
            totalCreditBalance += creditsSale["outstanding_amount"] 

        products = db.products.find()

        response = jsonify({'_id': lista[0]["_id"]
                            , 'description': lista[0]["description"]
                            , 'capital': lista[0]["capital"]
                            , 'capitalBefore': lista[0]["capitalBefore"]
                            , 'created_at': lista[0]["created_at"]
                            , 'expenses': expensesSum
                            , 'paymentsSale': paymentSale
                            , 'credits': credits
                            , 'payments': pay
                            , 'creditBalance': totalCreditBalance
                            })
        return response# Response(json_util.dumps(response), mimetype='application/json')
