from utils.db import db

class Pregunta(db.Model):
    __tablename__ = 'pregunta'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), nullable=True)
    descripcion = db.Column(db.String(255), nullable=True)

    # Constructor de la clase
    def __init__(self, codigo, descripcion):
        self.codigo = codigo
        self.descripcion = descripcion
