from flask import Blueprint
from flask import jsonify
from flask import request

from database import get_connection

entregas_bp = Blueprint(
    "entregas",
    __name__
)


@entregas_bp.route('/entregas', methods=['GET'])
def obtener_entregas():

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            e.id,
            m.nombre AS material,
            p.nombre AS punto,
            e.peso,
            e.fecha,
            e.responsable,
            e.estado
        FROM entregas e
        INNER JOIN materiales m
            ON e.material_id = m.id
        INNER JOIN puntos_acopio p
            ON e.punto_id = p.id
    """)

    entregas = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(entregas)


@entregas_bp.route('/entregas', methods=['POST'])
def crear_entrega():

    data = request.get_json()

    punto_id = data['punto_id']
    material_id = data['material_id']
    peso = data['peso']
    fecha = data['fecha']
    responsable = data['responsable']
    estado = data['estado']

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO entregas
        (
            punto_id,
            material_id,
            peso,
            fecha,
            responsable,
            estado
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
    """,
    (
        punto_id,
        material_id,
        peso,
        fecha,
        responsable,
        estado
    ))

    connection.commit()

    cursor.close()
    connection.close()
    return {
        "mensaje": "Entrega registrada correctamente"
    }, 201


@entregas_bp.route('/reportes/materiales', methods=['GET'])
def reporte_materiales():

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            m.nombre AS material,
            SUM(e.peso) AS total
        FROM entregas e
        INNER JOIN materiales m
            ON e.material_id = m.id
        GROUP BY m.nombre
    """)

    reporte = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(reporte)


@entregas_bp.route('/reportes/puntos', methods=['GET'])
def reporte_puntos():

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            p.nombre AS punto,
            SUM(e.peso) AS total
        FROM entregas e
        INNER JOIN puntos_acopio p
            ON e.punto_id = p.id
        GROUP BY p.nombre
    """)

    reporte = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(reporte)


@entregas_bp.route('/reportes/fechas')
def reporte_fechas():

    fecha_inicio = request.args.get('inicio')
    fecha_fin = request.args.get('fin')

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            m.nombre AS material,
            SUM(e.peso) AS total
        FROM entregas e
        INNER JOIN materiales m
            ON e.material_id = m.id
        WHERE e.fecha BETWEEN %s AND %s
        GROUP BY m.nombre
    """,
    (
        fecha_inicio,
        fecha_fin
    ))

    reporte = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(reporte)