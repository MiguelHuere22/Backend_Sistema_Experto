from utils.ma import ma
from models.especialidad import Especialidad
from marshmallow import fields

class EspecialidadSchema(ma.Schema):
    class Meta:
        model = Especialidad
        fields = ('id', 'nombre', 'descripcion','recomendaciones')

especialidad_schema = EspecialidadSchema()
especialidades_schema = EspecialidadSchema(many=True)
