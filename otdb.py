import requests
import html
from models.quiz import QuizModel
from db import db

def fetch_and_save_questions(amount=50, category=14, num_repeats=20):
    url = "https://opentdb.com/api.php?"
    parameters = {
        'amount': amount,
        'type': 'multiple'
    }
    if category:
        parameters['category'] = category

    # Conjunto para armazenar perguntas únicas (para evitar duplicatas)
    questions_set = set()

    for _ in range(num_repeats):  # repetindo a requisição num_repeats vezes
        response = requests.get(url, params=parameters)

        if response.status_code == 200:
            questions = response.json()['results']

            # Filtrando perguntas que contenham "Star Trek" e ainda não estão no conjunto
            star_trek_questions = [q for q in questions if "Star Trek" in q["question"] and q["question"] not in questions_set]

            for q in star_trek_questions:
                questions_set.add(q["question"])  # adicionar pergunta ao conjunto

            print(star_trek_questions)

            try:
                for q in star_trek_questions:
                    question = html.unescape(q['question'])
                    correct_answer = html.unescape(q['correct_answer'])
                    incorrect_answers = ','.join([html.unescape(ans) for ans in q['incorrect_answers']])

                    quiz_entry = QuizModel(question=question, correct_answer=correct_answer, incorrect_answers=incorrect_answers)
                    db.session.add(quiz_entry)
            except Exception as e:
                db.session.rollback()
                print(f"Error saving questions: {e}")

            db.session.commit()
        else:
            print(f"Failed to get questions. Status code: {response.status_code}")
