from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128)) # Guardaremos um hash, não a senha

    # implementar um hash check

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    # ex: "Opção A; Opção B; Opção C"
    options = db.Column(db.string(255), nullable=False)
    correct_answer = db.Column(db.String(100), nullable=False)
