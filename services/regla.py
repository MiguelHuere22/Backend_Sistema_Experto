from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from models.regla import Regla
from schemas.regla_schema import regla_schema, reglas_schema

regla_routes = Blueprint("regla_routes", __name__)

# Crear Regla
@regla_routes.route('/regla', methods=['POST'])
def create_regla():
    id = request.json.get('id')  # Se obtiene el ID del JSON
    especialidad_id = request.json.get('especialidad_id')
    condiciones = request.json.get('condiciones')

    new_regla = Regla(id=id, especialidad_id=especialidad_id, condiciones=condiciones)

    db.session.add(new_regla)
    db.session.commit()

    result = regla_schema.dump(new_regla)

    data = {
        'message': 'Nueva regla creada!',
        'status': 201,
        'data': result
    }

    return make_response(jsonify(data), 201)

# Obtener todas las Reglas
@regla_routes.route('/regla', methods=['GET'])
def get_reglas():
    all_reglas = Regla.query.all()
    result = reglas_schema.dump(all_reglas)

    data = {
        'message': 'Todas las reglas',
        'status': 200,
        'data': result
    }

    return make_response(jsonify(data), 200)

# Obtener Regla por ID
@regla_routes.route('/regla/<int:id>', methods=['GET'])
def get_regla(id):
    regla = Regla.query.get(id)

    if not regla:
        data = {
            'message': 'Regla no encontrada',
            'status': 404
        }
        return make_response(jsonify(data), 404)

    result = regla_schema.dump(regla)

    data = {
        'message': 'Regla encontrada',
        'status': 200,
        'data': result
    }

    return make_response(jsonify(data), 200)

# Actualizar Regla
@regla_routes.route('/regla/<int:id>', methods=['PUT'])
def update_regla(id):
    regla = Regla.query.get(id)

    if not regla:
        data = {
            'message': 'Regla no encontrada',
            'status': 404
        }
        return make_response(jsonify(data), 404)
    regla.id=request.json.get('id')
    regla.especialidad_id = request.json.get('especialidad_id')
    regla.condiciones = request.json.get('condiciones')

    db.session.commit()

    result = regla_schema.dump(regla)

    data = {
        'message': 'Regla actualizada',
        'status': 200,
        'data': result
    }

    return make_response(jsonify(data), 200)

# Eliminar Regla
@regla_routes.route('/regla/<int:id>', methods=['DELETE'])
def delete_regla(id):
    regla = Regla.query.get(id)

    if not regla:
        data = {
            'message': 'Regla no encontrada',
            'status': 404
        }
        return make_response(jsonify(data), 404)

    db.session.delete(regla)
    db.session.commit()

    data = {
        'message': 'Regla eliminada',
        'status': 200
    }

    return make_response(jsonify(data), 200)
