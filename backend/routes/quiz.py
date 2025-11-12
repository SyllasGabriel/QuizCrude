from flask import Blueprint, jsonify, request, session
from flask_login import login_required, current_user
from models import db, Question # Assumindo a existência de models.py

quiz_bp = Blueprint('quiz_bp', __name__, url_prefix='/quiz')

def get_current_question_data(question):
    """Formata os dados da pergunta para JSON."""
    return {
        "id": question.id,
        "text": question.text,
        "options": {
            "A": question.option_a,
            "B": question.option_b,
            "C": question.option_c
        }
    }

@quiz_bp.route('/', methods=['GET'])
@login_required 
def quiz_home():
    """Retorna a pergunta atual e o status do quiz."""
    question_id = session.get('current_question', 1)
    question = Question.query.get(question_id)

    if not question:
        # Fim do quiz: solicita o redirecionamento para a rota de resultados
        return jsonify({
            "message": "Quiz concluído. Por favor, acesse /quiz/results.",
            "status": "completed"
        }), 200

    # Retorna a pergunta atual
    return jsonify({
        "status": "active",
        "current_question_number": question_id,
        "score": session.get('quiz_score', 0),
        "question": get_current_question_data(question)
    }), 200

@quiz_bp.route('/submit', methods=['POST'])
@login_required
def submit_answer():
    """Processa a resposta enviada pelo usuário."""
    data = request.get_json()
    user_answer = data.get('answer') # Espera 'A', 'B', ou 'C'

    question_id = session.get('current_question')
    question = Question.query.get(question_id)
    
    if not question or not user_answer:
        return jsonify({"message": "Dados de resposta incompletos ou quiz não iniciado."}), 400

    # 1. Checagem da Resposta
    is_correct = False
    if user_answer == question.correct_option:
        session['quiz_score'] += 1
        is_correct = True

    # 2. Avança para a próxima pergunta e retorna o status
    session['current_question'] = question_id + 1
    
    return jsonify({
        "message": "Resposta processada.",
        "correct": is_correct,
        "your_answer": user_answer,
        "correct_answer": question.correct_option,
        "new_score": session['quiz_score']
    }), 200

@quiz_bp.route('/results', methods=['GET'])
@login_required
def quiz_results():
    """Exibe o resultado final do quiz."""
    score = session.get('quiz_score', 0)
    total_questions = Question.query.count()
    
    # Limpa variáveis para permitir um novo quiz
    session.pop('quiz_score', None)
    session.pop('current_question', None)
    
    return jsonify({
        "message": "Resultado Final do Quiz",
        "score": score,
        "total_questions": total_questions,
        "percentage": (score / total_questions) * 100 if total_questions else 0
    }), 200