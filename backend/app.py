from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from models import db, User, Question # Importa os models
import click # pra custom commands

# blueprints
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

    CORS(app, supports_credentials=True)

    db.init_app(app)

    # setup flask-login
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    # Registra as rotas/blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(quiz_bp, url_prefix='/api/quiz')

    # comando custom para seedar o db
    @app.cli.command("seed-db")
    def seed_db():
        """Adiciona algumas perguntas para o banco de dados"""
        if Question.query.first():
            print("Database already seeded.")
            return
        
        questions_data = [
            Question(text="Qual é o líder dos Autobots?", options="Bumblebee; Megatron; Optimus Prime; Ironhide", correct_answer="Optimus Prime"),
            Question(text="Quem é o principal inimigo dos Autobots?", options="Starscream; Megatron; Shockwave; Soundwave", correct_answer="Megatron"),
            Question(text="Qual desses Transformers é um Camaro amarelo?", options="Ratchet; Ironhide; Bumblebee; Cliffjumper", correct_answer="Bumblebee"),
            Question(text="De qual planeta os Transformers vêm?", options="Cybertron; Earth; Krypton; Velocitron", correct_answer="Cybertron"),
            Question(text="Quem é o braço direito de Megatron?", options="Shockwave; Starscream; Soundwave; Devastator", correct_answer="Soundwave")
        ]
        db.session.bulk_save_objects(questions_data)
        db.session.commit()
        print("Database seeded with initial questions.")
    
    with app.app_context():
        # cria as tabelas no banco de dados
        db.create_all()
        print("Banco de dados inicializado e tabelas criadas.")

    return app

app = create_app()

if __name__ == '__main__':
    # Roda o servidor de desenvolvimento do Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
    