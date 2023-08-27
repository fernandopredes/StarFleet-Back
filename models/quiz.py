from db import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class QuizModel(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.String(200), nullable=False)
    incorrect_answers = db.Column(db.String(600), nullable=False)
