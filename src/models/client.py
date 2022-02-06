from marshmallow import Schema, fields

class domicilio(Schema):
    municipio : fields.String(required=False)
    colonia : fields.String(required=False)
    direccion : fields.String(required=False)
    codigoPostal : fields.String(required=False)
    referencia : fields.String(required=False)

class client(Schema):
    id:str
    primerNombre : fields.String(required=True)
    segundoNombre : fields.String(required=False)
    apellidos : fields.String(required=True)
    fechaNacimiento: fields.Time(required=False)
    rfc : fields.String(required=False)
    correo : fields.String(required=False)
    telefono : fields.String(required=False)
    domicilio : domicilio
