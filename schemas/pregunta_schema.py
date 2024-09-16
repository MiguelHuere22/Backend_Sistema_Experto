from utils.ma import ma
from models.pregunta import Pregunta
from marshmallow import fields

class PreguntaSchema(ma.Schema):
    class Meta:
        model = Pregunta
        fields = ('id',
                 'codigo',
                'descripcion')

pregunta_schema = PreguntaSchema()
preguntas_schema = PreguntaSchema(many=True)
