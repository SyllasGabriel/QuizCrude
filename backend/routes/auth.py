from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, current_user
from models import db, User # Importe as classes do seu models.py

# Cria um Blueprint para as rotas de autenticação
auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

# --- Rotas de Autenticação (AUTH) ---

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Lida com a entrada do usuário e inicia a sessão."""
    # 1. Se já estiver autenticado, redireciona para a página principal do quiz
    if current_user.is_authenticated:
        # Note que 'quiz_bp.quiz_home' assume que o Blueprint do quiz é 'quiz_bp'
        return redirect(url_for('quiz_bp.quiz_home')) 

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Busca o usuário no banco de dados
        user = User.query.filter_by(username=username).first()

        # 2. Verifica credenciais
        if user and user.check_password(password):
            login_user(user) # Inicia a sessão de forma segura (Flask-Login)
            
            # 3. Inicializa variáveis de estado do quiz na sessão
            session['quiz_score'] = 0     
            session['current_question'] = 1 
            
            flash(f'Bem-vindo(a), {username}!', 'success')
            return redirect(url_for('quiz_bp.quiz_home'))
        else:
            flash('Nome de usuário ou senha inválidos.', 'danger')
            
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Lida com o cadastro de novos usuários."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 1. Checa se o usuário já existe
        if User.query.filter_by(username=username).first():
            flash('Este nome de usuário já está em uso.', 'warning')
            return redirect(url_for('auth_bp.register'))
        
        # 2. Cria e salva o novo usuário
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('auth_bp.login'))

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    """Encerra a sessão do usuário."""
    if current_user.is_authenticated:
        logout_user() # Encerra a sessão (Flask-Login)
        # Limpa o estado do quiz, caso não tenha sido feito após os resultados
        session.pop('quiz_score', None)
        session.pop('current_question', None)
        
    flash('Você foi desconectado(a).', 'info')
    return redirect(url_for('auth_bp.login'))