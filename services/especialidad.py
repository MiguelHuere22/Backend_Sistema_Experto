from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from models.especialidad import Especialidad
from schemas.especialidad_schema import especialidad_schema, especialidades_schema

especialidad_routes = Blueprint("especialidad_routes", __name__)

# Crear Especialidad
@especialidad_routes.route('/especialidad', methods=['POST'])
def create_especialidad():
    id = request.json.get('id')  # Se obtiene el ID del JSON
    nombre = request.json.get('nombre')
    descripcion = request.json.get('descripcion')
    recomendaciones=recomendaciones.json.get('recomendaciones')

    new_especialidad = Especialidad(id=id, nombre=nombre, descripcion=descripcion, recomendaciones=recomendaciones)

    db.session.add(new_especialidad)
    db.session.commit()

    result = especialidad_schema.dump(new_especialidad)

    data = {
        'message': 'Nueva especialidad creada!',
        'status': 201,
        'data': result
    }

    return make_response(jsonify(data), 201)

# Obtener todas las Especialidades
@especialidad_routes.route('/especialidad', methods=['GET'])
def get_especialidades():
    all_especialidades = Especialidad.query.all()
    result = especialidades_schema.dump(all_especialidades)

    data = {
        'message': 'Todas las especialidades',
        'status': 200,
        'data': result
    }

    return make_response(jsonify(data), 200)

# Obtener Especialidad por ID
@especialidad_routes.route('/especialidad/<int:id>', methods=['GET'])
def get_especialidad(id):
    especialidad = Especialidad.query.get(id)

    if not especialidad:
        data = {
            'message': 'Especialidad no encontrada',
            'status': 404
        }
        return make_response(jsonify(data), 404)

    result = especialidad_schema.dump(especialidad)

    data = {
        'message': 'Especialidad encontrada',
        'status': 200,
        'data': result
    }

    return make_response(jsonify(data), 200)

# Actualizar Especialidad
@especialidad_routes.route('/especialidad/<int:id>', methods=['PUT'])
def update_especialidad(id):
    especialidad = Especialidad.query.get(id)

    if not especialidad:
        data = {
            'message': 'Especialidad no encontrada',
            'status': 404
        }
        return make_response(jsonify(data), 404)
    especialidad.id=request.json.get('id')
    especialidad.nombre = request.json.get('nombre')
    especialidad.descripcion = request.json.get('descripcion')
    especialidad.recomendaciones=request.json.get('recomendaciones')

    db.session.commit()

    result = especialidad_schema.dump(especialidad)

    data = {
        'message': 'Especialidad actualizada',
        'status': 200,
        'data': result
    }

    return make_response(jsonify(data), 200)

# Eliminar Especialidad
@especialidad_routes.route('/especialidad/<int:id>', methods=['DELETE'])
def delete_especialidad(id):
    especialidad = Especialidad.query.get(id)

    if not especialidad:
        data = {
            'message': 'Especialidad no encontrada',
            'status': 404
        }
        return make_response(jsonify(data), 404)

    db.session.delete(especialidad)
    db.session.commit()

    data = {
        'message': 'Especialidad eliminada',
        'status': 200
    }

    return make_response(jsonify(data), 200)
