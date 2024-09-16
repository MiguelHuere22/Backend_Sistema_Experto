from utils.db import db

class Especialidad(db.Model):
    __tablename__ = 'especialidad'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=True)
    descripcion = db.Column(db.String(255), nullable=True)  # Campo "descripcion"
    recomendaciones = db.Column(db.String(1000000), nullable=True) 

    # Constructor de la clase
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion
