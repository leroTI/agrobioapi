from os import path
from flask_restx import Namespace

ingredientns = Namespace(
    path='/ingredients',
    name='ingredients',
    description='Ingredientes'
)

connect = Namespace(
    path='/connect',
    name='connect',
    description='Integraccion Consul'
)

products = Namespace(
    path='/products',
    name='products',
    description='Productos'
)

sale = Namespace(
    path='/sale',
    name='sale',
    description='venta de productos'
)

sesion = Namespace(
    path='/sesion',
    name='sesion',
    description='Sesión'
)

client = Namespace(
    path='/client',
    name='client',
    description='Clientes'
)


bills = Namespace(
    path='/bills',
    name='bills',
    description='Gastos'
)

expenses = Namespace(
    path='/expense',
    name='expense',
    description='Gastos Oerativos'
)