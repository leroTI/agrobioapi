from marshmallow import Schema, fields

class capitalNeto(Schema):
    _id=fields.String(required=False)
    description = fields.String(required=True)
    capital=fields.Decimal(required=False)
    created_at:fields.Date(required=False)