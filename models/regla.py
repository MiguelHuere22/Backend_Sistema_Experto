from utils.db import db
from models.especialidad import Especialidad

class Regla(db.Model):
    __tablename__ = 'regla'

    id = db.Column(db.Integer, primary_key=True)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidad.id'), nullable=True)
    condiciones = db.Column(db.String(255), nullable=True)

    especialidad = db.relationship('Especialidad', backref='rEGLA')

    # Constructor de la clase
    def __init__(self, especialidad_id, condiciones):
        self.especialidad_id = especialidad_id
        self.condiciones = condiciones
