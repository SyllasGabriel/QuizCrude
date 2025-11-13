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
            Question(text="Qual a capital da França?", options="Londres; Paris; Roma; Berlim", correct_answer="Paris"),
            Question(text="Qual é o maior planeta do nosso sistema solar?", options="Terra; Júpiter; Marte; Saturno", correct_answer="Júpiter"),
            Question(text="Quem escreveu 'Dom Quixote'?", options="Machado de Assis; Miguel de Cervantes; William Shakespeare; Jorge Luis Borges", correct_answer="Miguel de Cervantes"),
            Question(text="Qual elemento tem o símbolo químico 'O'?", options="Ouro; Oxigênio; Ósmio; Prata", correct_answer="Oxigênio"),
            Question(text="Em que ano o homem pisou na Lua pela primeira vez?", options="1965; 1969; 1972; 1980", correct_answer="1969")
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
    