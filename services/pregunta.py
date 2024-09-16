from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from models.pregunta import Pregunta
from schemas.pregunta_schema import pregunta_schema, preguntas_schema

pregunta_routes = Blueprint("pregunta_routes", __name__)

# Crear Pregunta
@pregunta_routes.route('/pregunta', methods=['POST'])
def create_pregunta():
    id = request.json.get('id')  # Se obtiene el ID del JSON
    codigo = request.json.get('codigo')
    descripcion = request.json.get('descripcion')

    new_pregunta = Pregunta(id=id, codigo=codigo, descripcion=descripcion)

    db.session.add(new_pregunta)
    db.session.commit()

    result = pregunta_schema.dump(new_pregunta)

    data = {
        'message': 'Nueva pregunta creada!',
        'status': 201,
        'data': result
    }

    return make_response(jsonify(data), 201)

# Obtener todas las Preguntas
@pregunta_routes.route('/pregunta', methods=['GET'])
def get_preguntas():
    all_preguntas = Pregunta.query.all()
    result = preguntas_schema.dump(all_preguntas)

    data = {
        'message': 'Todas las preguntas',
        'status': 200,
        'data': result
    }

    return make_response(jsonify(data), 200)

# Obtener Pregunta por ID
@pregunta_routes.route('/pregunta/<int:id>', methods=['GET'])
def get_pregunta(id):
    pregunta = Pregunta.query.get(id)

    if not pregunta:
        data = {
            'message': 'Pregunta no encontrada',
            'status': 404
        }
        return make_response(jsonify(data), 404)

    result = pregunta_schema.dump(pregunta)

    data = {
        'message': 'Pregunta encontrada',
        'status': 200,
        'data': result
    }

    return make_response(jsonify(data), 200)

# Actualizar Pregunta
@pregunta_routes.route('/pregunta/<int:id>', methods=['PUT'])
def update_pregunta(id):
    pregunta = Pregunta.query.get(id)

    if not pregunta:
        data = {
            'message': 'Pregunta no encontrada',
            'status': 404
        }
        return make_response(jsonify(data), 404)
    
    pregunta.id=request.json.get('id')
    pregunta.codigo = request.json.get('codigo')
    pregunta.descripcion = request.json.get('descripcion')

    db.session.commit()

    result = pregunta_schema.dump(pregunta)

    data = {
        'message': 'Pregunta actualizada',
        'status': 200,
        'data': result
    }

    return make_response(jsonify(data), 200)

# Eliminar Pregunta
@pregunta_routes.route('/pregunta/<int:id>', methods=['DELETE'])
def delete_pregunta(id):
    pregunta = Pregunta.query.get(id)

    if not pregunta:
        data = {
            'message': 'Pregunta no encontrada',
            'status': 404
        }
        return make_response(jsonify(data), 404)

    db.session.delete(pregunta)
    db.session.commit()

    data = {
        'message': 'Pregunta eliminada',
        'status': 200
    }

    return make_response(jsonify(data), 200)
