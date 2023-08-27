import os
import secrets
import requests

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_cors import CORS

from db import db
import models
import cloudinary

from resources.user import blp as UserBlueprint
from resources.post import blp as PostBlueprint
from resources.quiz import blp as QuizBlueprint

CATEGORY_ID_FOR_STAR_TREK = None

def fetch_star_trek_questions():
    from otdb import fetch_and_save_questions
    fetch_and_save_questions(amount=25, category=CATEGORY_ID_FOR_STAR_TREK)

def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    app.config["API_TITLE"] = "StarFleet API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config['API_SPEC_OPTIONS'] = {
        'security':[{"bearerAuth": []}],
        'components':{
            "securitySchemes":
                {
                    "bearerAuth": {
                        "type":"http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                }
        }
    }

    db.init_app(app)
    api = Api(app)

    # Enable CORS
    CORS(app)

    cloudinary.config(
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key = os.getenv('CLOUDINARY_API_KEY'),
    api_secret = os.getenv('CLOUDINARY_API_SECRET')
)

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt = JWTManager(app)

    # JWT configuration starts

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "O token venceu.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Verificação falhou.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Não possui um token de acesso.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "O token não é novo.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "O token foi revogado.", "error": "token_revoked"}
            ),
            401,
        )
    # JWT configuration ends

    with app.app_context():
        db.create_all()
        fetch_star_trek_questions()

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(PostBlueprint)
    api.register_blueprint(QuizBlueprint)


    return app
