from flask import Blueprint, request, jsonify, session
from flask_login import login_required
from models import db, Question # Importa os modelos de dados

# Cria o Blueprint para as rotas, o prefixo de URL será definido em app.py
quiz_bp = Blueprint('quiz_bp', __name__)

def format_question_data(question):
    """Formata a pergunta, excluindo a resposta correta."""
    return {
        "id": question.id,
        "text": question.text,
        # Assume que as opções estão separadas por "; "
        "options": question.options.split('; ') 
    }

@quiz_bp.route('/question', methods=['GET'])
@login_required 
def get_current_question():
    """Retorna a próxima pergunta a ser respondida."""
    # Garante que a sessão tenha um ID de pergunta (inicia em 1)
    question_id = session.get('current_question', 1) 
    question = db.session.get(Question, question_id)

    if not question:
        # Se não houver mais perguntas, indica que o quiz acabou
        return jsonify({
            "status": "completed",
            "message": "Quiz finalizado. Acesse /api/quiz/results."
        }), 200

    return jsonify({
        "status": "active",
        "current_question_number": question_id,
        "score": session.get('quiz_score', 0),
        "question": format_question_data(question)
    }), 200

@quiz_bp.route('/submit', methods=['POST'])
@login_required
def submit_answer():
    """Processa a resposta e avança para a próxima pergunta."""
    data = request.get_json()
    user_answer = data.get('answer') 

    # ID da pergunta que o usuário acabou de responder (ID atual)
    answered_q_id = session.get('current_question', 1) 
    answered_question = db.session.get(Question, answered_q_id) 

    if not answered_question or not user_answer:
        return jsonify({"message": "Resposta inválida ou sessão fora de sincronia."}), 400

    is_correct = False
    
    # Verifica a resposta
    if user_answer == answered_question.correct_answer:
        session['quiz_score'] += 1
        is_correct = True
        
    # Avança para a próxima pergunta
    session['current_question'] += 1
    
    return jsonify({
        "message": "Resposta processada.",
        "correct": is_correct,
        "new_score": session['quiz_score']
    }), 200

@quiz_bp.route('/results', methods=['GET'])
@login_required
def quiz_results():
    """Retorna o resultado final do quiz e limpa a sessão."""
    score = session.get('quiz_score', 0)
    total_questions = Question.query.count()
    
    # Limpa as variáveis para permitir que o usuário inicie um novo quiz
    session.pop('quiz_score', None)
    session.pop('current_question', None)
    
    return jsonify({
        "message": "Resultado Final",
        "score": score,
        "total_questions": total_questions,
        "percentage": (score / total_questions) * 100 if total_questions else 0
    }), 200