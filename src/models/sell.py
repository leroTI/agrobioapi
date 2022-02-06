from datetime import date
from typing import List
from marshmallow import Schema, fields

class saleproduct:
    id: str
    descripcion: str
    precio: int
    cantidad: int
    importe: int

class sell(Schema):
    efectivo: fields.Float(required=True)
    monto: fields.Float(required=True)
    credit: fields.Float(required=True)
    id_region: fields.Integer(required=True)
    total: fields.Float(required=True)
    cambio: fields.Float(required=True)
    sale_products: List[saleproduct]
    created_at: fields.Date(required=True)

