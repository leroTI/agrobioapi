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