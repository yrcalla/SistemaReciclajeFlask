from flask import Blueprint
from flask import jsonify
from flask import request

from database import get_connection

puntos_bp = Blueprint(
    "puntos",
    __name__
)


@puntos_bp.route('/puntos', methods=['GET'])
def obtener_puntos():

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM puntos_acopio
    """)

    puntos = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(puntos)


@puntos_bp.route('/puntos', methods=['POST'])
def crear_punto():

    data = request.get_json()

    nombre = data['nombre']
    direccion = data['direccion']

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO puntos_acopio
        (
            nombre,
            direccion
        )
        VALUES
        (
            %s,
            %s
        )
    """, (nombre, direccion))

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "mensaje": "Punto creado correctamente"
    }, 201


@puntos_bp.route('/puntos/<int:id>', methods=['PUT'])
def actualizar_punto(id):

    data = request.get_json()

    nombre = data['nombre']
    direccion = data['direccion']

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE puntos_acopio
        SET nombre = %s,
            direccion = %s
        WHERE id = %s
    """, (nombre, direccion, id))

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "mensaje": "Punto actualizado"
    }


@puntos_bp.route('/puntos/<int:id>', methods=['DELETE'])
def eliminar_punto(id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM puntos_acopio
        WHERE id = %s
    """, (id,))

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "mensaje": "Punto eliminado"
    }
