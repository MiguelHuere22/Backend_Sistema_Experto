from utils.ma import ma
from models.regla import Regla
from marshmallow import fields
from schemas.especialidad_schema import EspecialidadSchema

class ReglaSchema(ma.Schema):
    class Meta:
        model = Regla
        fields = ('id', 'especialidad_id', 'condiciones', 'especialidad')

    especialidad=ma.Nested(EspecialidadSchema)

regla_schema = ReglaSchema()
reglas_schema = ReglaSchema(many=True)
