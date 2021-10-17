from flask_restplus import Namespace

ingredients = Namespace(
    path='/ingredients',
    name='ingredients',
    description='Ingredientes'
)

connect = Namespace(
    path='/connect',
    name='connect',
    description='Integraccion Consul'
)