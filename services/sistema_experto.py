from flask import Blueprint, request, jsonify, make_response
from flask_cors import CORS  # <-- Añadir esta línea
from models.pregunta import Pregunta
from models.regla import Regla
from models.especialidad import Especialidad
from experta import KnowledgeEngine, Fact
from utils.db import db
import re  # Importamos el módulo para usar expresiones regulares

# Crear un Blueprint para las rutas del sistema experto
sistema_experto_routes = Blueprint("sistema_experto_routes", __name__)

# Habilitar CORS en la aplicación Flask
CORS(sistema_experto_routes)  # <-- Añadir esta línea

# Definimos los hechos (fact) para el sistema experto
class PerfilUsuario(Fact):
    """Información del perfil del usuario"""
    pass

# Sistema experto basado en las reglas obtenidas de la base de datos
class SistemaExpertoEspecializaciones(KnowledgeEngine):

    def __init__(self, reglas):
        super().__init__()
        self.exactas = []
        self.probables = []
        self.reglas = reglas

    # Método para cargar y procesar las reglas manualmente
    def procesar_reglas_manual(self, respuestas):
        for especialidad, condiciones in self.reglas:
            condiciones_dict = {str(cond.split('=')[0]): str(cond.split('=')[1]) for cond in condiciones.split(',')}
            
            # Verificamos si todas las condiciones se cumplen con las respuestas del usuario
            if all(respuestas.get(codigo) == valor for codigo, valor in condiciones_dict.items()):
                # Si cumple todas las condiciones, lo marcamos como exacta
                self.exactas.append(especialidad)
            else:
                # Si no cumple todas pero se aproxima, lo agregamos como probable con la cantidad de coincidencias
                coincidencias = sum(respuestas.get(codigo) == valor for codigo, valor in condiciones_dict.items())
                if coincidencias > 0:
                    self.probables.append((especialidad, coincidencias))

    # Mostrar todas las recomendaciones
    def mostrar_recomendaciones(self, respuestas_usuario):
        if self.exactas:
            # Si hay especialidades exactas, mostramos el número exacto de especialidades encontradas
            num_especialidades = len(self.exactas)
            if num_especialidades == 1:
                mensaje = "Se encontró 1 especialidad exacta."
            else:
                mensaje = f"Se encontraron {num_especialidades} especialidades exactas."
            return {
                "mensaje": mensaje,
                "especialidades": self.exactas
            }
        else:
            # Si no hay exactas, buscamos las especialidades con mayor coincidencias
            if self.probables:
                # Ordenamos las probables por el número de coincidencias
                max_coincidencias = max(self.probables, key=lambda x: x[1])[1]
                mejores_especialidades = [especialidad for especialidad, coincidencias in self.probables if coincidencias == max_coincidencias]
                
                num_probables = len(mejores_especialidades)
                if num_probables == 1:
                    mensaje = f"No se encontraron especialidades exactas. Se recomienda la especialidad con {max_coincidencias} coincidencias."
                else:
                    mensaje = f"No se encontraron especialidades exactas. Se recomiendan {num_probables} especialidades con {max_coincidencias} coincidencias."
                    
                return {
                    "mensaje": mensaje,
                    "especialidades": mejores_especialidades
                }
            else:
                # Si no hay ninguna especialidad probable
                return {
                    "mensaje": "No se encontró una especialidad probable.",
                    "especialidades": []
                }


# Función para generar recomendaciones desde el campo de la base de datos
def obtener_recomendaciones_desde_bd(especialidad):
    especialidad_obj = Especialidad.query.filter_by(nombre=especialidad).first()
    return especialidad_obj.recomendaciones if especialidad_obj else "Recomendación no disponible."


@sistema_experto_routes.route('/procesar_respuestas', methods=['POST'])
def procesar_respuestas():
    # Obtener las respuestas del usuario desde el request JSON
    respuestas = request.json.get('respuestas')
    
    # Obtener las preguntas y reglas desde la base de datos
    reglas = obtener_reglas()
    
    # Crear el sistema experto con las reglas
    sistema = SistemaExpertoEspecializaciones(reglas)
    
    # Procesar las reglas con las respuestas del usuario
    sistema.procesar_reglas_manual(respuestas)
    
    # Obtener las recomendaciones del sistema experto
    recomendaciones = sistema.mostrar_recomendaciones(respuestas)
    
    # Si hay especialidades recomendadas, buscar también la descripción y las recomendaciones de la base de datos
    if recomendaciones["especialidades"]:
        recomendaciones_extra = {}
        descripciones_especialidades = {}

        for especialidad in recomendaciones["especialidades"]:
            # Obtener la descripción y las recomendaciones desde la base de datos
            especialidad_obj = Especialidad.query.filter_by(nombre=especialidad).first()
            descripciones_especialidades[especialidad] = especialidad_obj.descripcion if especialidad_obj else "Descripción no disponible."
            
            # Obtener recomendaciones del campo "recomendaciones"
            recomendaciones_extra[especialidad] = obtener_recomendaciones_desde_bd(especialidad)
        
        # Ajustar el orden de los datos en la respuesta
        data = {
            'recomendaciones': {
                'especialidades': recomendaciones["especialidades"],
                'descripciones': descripciones_especialidades,
                'recomendaciones_detalladas': recomendaciones_extra,
                'mensaje': recomendaciones["mensaje"]
            }
        }
    else:
        # Si no hay especialidades recomendadas
        data = {
            'recomendaciones': recomendaciones
        }
    
    # Enviar la respuesta como JSON
    return make_response(jsonify(data), 200)


# Obtener las preguntas desde la base de datos
def obtener_preguntas():
    preguntas = Pregunta.query.all()
    return [(pregunta.codigo, pregunta.descripcion) for pregunta in preguntas]

# Obtener las reglas desde la base de datos
def obtener_reglas():
    reglas = db.session.query(Regla, Especialidad).join(Especialidad).all()
    return [(regla.Especialidad.nombre, regla.Regla.condiciones) for regla in reglas]
