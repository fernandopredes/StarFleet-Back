from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from db import db
from models.quiz import QuizModel
from schemas import QuizSchema

blp = Blueprint("Quizzes", __name__, description="Operações com Quizzes")

@blp.route('/quizzes')
class QuizList(MethodView):
    @jwt_required()
    @blp.response(200, QuizSchema(many=True), description="Sucesso. Retorna todas as perguntas.")
    def get(self):
        """Busca todas as perguntas"""
        quizzes = QuizModel.query.all()
        quiz_schema = QuizSchema(many=True)
        return quiz_schema.dump(quizzes)

@blp.route('/quizzes/<int:quiz_id>')
class Quiz(MethodView):
    @jwt_required()
    @blp.response(200, QuizSchema, description="Sucesso. Retorna a pergunta pelo id selecionado")
    def get(self, quiz_id):
        """Pega apenas uma pergunta"""
        quiz = QuizModel.query.get_or_404(quiz_id)
        return quiz
