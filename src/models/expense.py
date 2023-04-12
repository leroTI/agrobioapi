from marshmallow import Schema, fields

class expense(Schema):
    _id=fields.String(required=False)
    create_at = fields.Date(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    importe = fields.Float(required=True)