from flask import Flask
from flask_cors import CORS
from models import db # Importa a instância do banco de dados de models.py

from routes.auth import auth_bp
from routes.quiz import quiz_bp

def create_app():
    """
    Cria e configura uma instância da aplicação Flask.
    """
    app = Flask(__name__)
    
    # Chave secreta para o Flask
    app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-segura'
    
    # configuração banco de dados SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)

    db.init_app(app)
    
    # Registra as rotas de autenticação (de routes/auth.py) na aplicação
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # Registra as rotas do quiz (de routes/quiz.py) na aplicação
    app.register_blueprint(quiz_bp, url_prefix='/api/quiz')
    
    with app.app_context():
        # cria as tabelas no banco de dados se elas não existirem, com base em models.py
        db.create_all()
        print("Banco de dados inicializado e tabelas criadas (se necessário).")

    return app

app = create_app()

if __name__ == '__main__':
    # Roda o servidor de desenvolvimento do Flask
    app.run(host='0.0.0.0', port=5000, debug=True)