from flask import Flask
from flask_jwt_extended import JWTManager

from routes.materiales import materiales_bp
from routes.puntos import puntos_bp
from routes.entregas import entregas_bp

from routes.auth import auth_bp

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "reciclaje2026"

jwt = JWTManager(app)

app.register_blueprint(materiales_bp)
app.register_blueprint(puntos_bp)
app.register_blueprint(entregas_bp)

app.register_blueprint(auth_bp)

@app.route('/')
def inicio():

    return {
        "mensaje":"Sistema de Gestión de Residuos"
    }

if __name__ == '__main__':
    app.run(debug=True)