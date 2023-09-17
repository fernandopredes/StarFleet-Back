import csv
from models.quiz import QuizModel
from db import db

def load_and_save_questions_from_csv(file_path='./questions.csv'):
    questions_set = set()

    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            question = row["question"]

            if question not in questions_set:
                questions_set.add(question)

                # Verificar se a pergunta já existe no banco de dados
                existing_question = QuizModel.query.filter_by(question=question).first()
                if existing_question:
                    print(f"Question '{question}' already exists in the database.")
                    continue

                correct_answer = row["correct_answer"]
                incorrect_answers = row["incorrect_answers"]

                try:
                    quiz_entry = QuizModel(question=question, correct_answer=correct_answer, incorrect_answers=incorrect_answers)
                    db.session.add(quiz_entry)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(f"Error saving questions: {e}")

        print(f"{len(questions_set)} unique questions processed.")
