from flask import Blueprint
from flask import request
from flask import jsonify

from database import get_connection

materiales_bp = Blueprint(
    'materiales',
    __name__
)


# =======================
# GET
# =======================

@materiales_bp.route('/materiales', methods=['GET'])
def obtener_materiales():

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM materiales
    """)

    materiales = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(materiales)


# =======================
# POST
# =======================

@materiales_bp.route('/materiales', methods=['POST'])
def crear_material():

    data = request.get_json()

    nombre = data['nombre']

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO materiales(nombre)
        VALUES(%s)
    """, (nombre,))

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "mensaje": "Material creado correctamente"
    }, 201


# =======================
# PUT
# =======================

@materiales_bp.route('/materiales/<int:id>', methods=['PUT'])
def actualizar_material(id):

    data = request.get_json()

    nombre = data['nombre']

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE materiales
        SET nombre=%s
        WHERE id=%s
    """, (nombre, id))

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "mensaje": "Material actualizado"
    }


# =======================
# DELETE
# =======================

@materiales_bp.route('/materiales/<int:id>', methods=['DELETE'])
def eliminar_material(id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM materiales
        WHERE id=%s
    """, (id,))

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "mensaje": "Material eliminado"
    }
    