from flask import Blueprint, jsonify, request, session
from flask_login import login_user, logout_user, current_user
from models import db, User # Assumindo a existência de models.py

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    # 1. Obter dados do corpo da requisição JSON
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Dados de login incompletos."}), 400

    user = User.query.filter_by(username=username).first()

    # 2. Verificar credenciais
    if user and user.check_password(password):
        login_user(user)
        # Inicializa o estado do quiz na sessão APÓS o login
        session['quiz_score'] = 0     
        session['current_question'] = 1 
        
        return jsonify({
            "message": "Login realizado com sucesso.",
            "user_id": user.id,
            "username": user.username,
            "is_logged_in": True
        }), 200
    else:
        return jsonify({"message": "Nome de usuário ou senha inválidos."}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Dados de registro incompletos."}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Usuário já existe."}), 409
    
    # 1. Cria e salva o novo usuário
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "Usuário criado com sucesso. Faça login."}), 201

@auth_bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user() 
        # Limpa o estado do quiz
        session.pop('quiz_score', None)
        session.pop('current_question', None)
        
    return jsonify({"message": "Logout realizado com sucesso."}), 200