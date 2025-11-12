from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user
from models import db, Question # Importe as classes do seu models.py

# Cria um Blueprint para as rotas do quiz
quiz_bp = Blueprint('quiz_bp', __name__, url_prefix='/quiz')

# --- Funções Auxiliares para o Quiz ---

def initialize_quiz_session():
    """Inicializa ou reseta as variáveis de sessão para um novo quiz."""
    session['quiz_score'] = 0
    session['current_question'] = 1
    # Opcional: session['questions_list'] = [q.id for q in Question.query.all()]
    # Isso seria útil para embaralhar as perguntas

# --- Rotas do Quiz ---

@quiz_bp.route('/')
@login_required 
def quiz_home():
    """
    Rota principal do quiz. 
    Redireciona para a próxima pergunta ou para o resultado final.
    """
    # Garante que a sessão do quiz esteja inicializada
    if 'current_question' not in session:
        initialize_quiz_session()

    question_id = session.get('current_question')
    question = Question.query.get(question_id)

    if not question:
        # Fim do quiz: Redireciona para a rota de resultados
        return redirect(url_for('quiz_bp.quiz_results'))

    # Renderiza a template com a pergunta atual
    return render_template('quiz.html', 
                           question=question, 
                           current_q_num=question_id,
                           score=session.get('quiz_score', 0))

@quiz_bp.route('/submit', methods=['POST'])
@login_required
def submit_answer():
    """Processa a resposta enviada pelo usuário."""
    user_answer = request.form.get('answer')
    question_id = session.get('current_question')
    question = Question.query.get(question_id)
    
    if not question or not user_answer:
        flash("Erro ao processar a resposta.", 'danger')
        return redirect(url_for('quiz_bp.quiz_home'))

    # 1. Checagem da Resposta
    if user_answer == question.correct_option:
        session['quiz_score'] += 1
        flash('Resposta Correta! ✔️', 'success')
    else:
        flash(f"Resposta Incorreta. A correta era **{question.correct_option}**.", 'danger')

    # 2. Avança para a próxima pergunta e redireciona
    session['current_question'] = question_id + 1
    
    return redirect(url_for('quiz_bp.quiz_home'))

@quiz_bp.route('/results')
@login_required
def quiz_results():
    """Exibe o resultado final do quiz."""
    score = session.get('quiz_score', 0)
    total_questions = Question.query.count()
    
    # Limpa as variáveis de sessão para que um novo quiz possa ser iniciado
    session.pop('quiz_score', None)
    session.pop('current_question', None)
    
    return render_template('resultado.html', score=score, total=total_questions)

@quiz_bp.route('/reset')
@login_required
def reset_quiz():
    """Permite que o usuário reinicie o quiz a qualquer momento."""
    initialize_quiz_session()
    flash("Quiz reiniciado!", 'info')
    return redirect(url_for('quiz_bp.quiz_home'))