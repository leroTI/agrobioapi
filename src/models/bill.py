from marshmallow import Schema, fields

class bill(Schema):
    # _id =  fields.String(required=False)
    _id=fields.String(required=False)
    name = fields.String(required=True)