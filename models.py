from flask_admin import BaseView, expose, ModelView
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Produtos(db.Model):
    __tablename__ = "Produtos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Numeric(10,2), nullable=False)
    categoria = db.Column(db.String(50))
    estoque = db.Column(db.Integer, default=0)
    id_imagem = db.Column(db.String(20))

class Usuarios(db.Model):
    __tablename__ = "Usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome= db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, default=False)