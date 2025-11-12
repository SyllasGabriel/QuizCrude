from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, current_user
from models import db, User # Importa os modelos de dados
from sqlalchemy.exc import IntegrityError

# Cria o Blueprint para as rotas, o prefixo de URL será definido em app.py
auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registra um novo usuário."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Nome de usuário e senha são obrigatórios."}), 400

    new_user = User(username=username)
    new_user.set_password(password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        # Erro comum se o username já existir (unique=True)
        return jsonify({"message": "Nome de usuário já existe."}), 409
    
    return jsonify({"message": "Registro bem-sucedido. Faça login."}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Autentica o usuário e inicia a sessão."""
    if current_user.is_authenticated:
        return jsonify({"message": "Você já está logado."}), 200

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        login_user(user) 
        
        # Inicializa o estado do quiz na sessão para o novo usuário
        session['quiz_score'] = 0     
        session['current_question'] = 1 
        
        return jsonify({
            "message": "Login bem-sucedido.",
            "username": user.username,
        }), 200
    else:
        return jsonify({"message": "Credenciais inválidas."}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Encerra a sessão do usuário."""
    if current_user.is_authenticated:
        logout_user() 
        # Limpa o estado do quiz da sessão
        session.pop('quiz_score', None)
        session.pop('current_question', None)
        
    return jsonify({"message": "Logout bem-sucedido."}), 200