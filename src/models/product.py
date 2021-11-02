from marshmallow import Schema, fields

from models.ingredient import ingredient

class product(Schema):
    _id =  fields.String(required=False)
    name = fields.String(required=True)
    idregion = fields.Integer(required=True)
    totalbuy = fields.Float(required=True)
    totalkgbuy = fields.Float(required=True)
    ingredients = fields.Raw()
    adicional  = fields.Raw()