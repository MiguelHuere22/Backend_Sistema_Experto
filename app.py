from flask import Flask
from utils.db import db
from utils.ma import ma  # Importamos Marshmallow para la serialización
from services.pregunta import pregunta_routes
from services.especialidad import especialidad_routes
from services.regla import regla_routes
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping  # Parche temporal para el problema con experta
from services.sistema_experto import sistema_experto_routes
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Importamos CORS
from config import DATABASE_CONNECTION

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Evitar mensajes de advertencia

# Habilitar CORS en toda la aplicación
CORS(app)  # Aplicar CORS globalmente a todas las rutas

# Inicializamos las extensiones
db.init_app(app)
ma.init_app(app)

# Registramos los blueprints (rutas) para cada entidad
app.register_blueprint(pregunta_routes)
app.register_blueprint(especialidad_routes)
app.register_blueprint(regla_routes)
app.register_blueprint(sistema_experto_routes)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
