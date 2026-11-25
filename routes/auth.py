from flask import Blueprint
from flask import request

from flask_jwt_extended import create_access_token

from database import get_connection

auth_bp = Blueprint(
    "auth",
    __name__
)

@auth_bp.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    correo = data['correo']
    password = data['password']

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM usuarios
        WHERE correo=%s
        AND password=%s
    """,
    (
        correo,
        password
    ))

    usuario = cursor.fetchone()

    cursor.close()
    connection.close()

    if usuario:

        token = create_access_token(
            identity=usuario['correo']
        )

        return {
            "token": token
        }

    return {
        "mensaje":"Credenciales incorrectas"
    },401


