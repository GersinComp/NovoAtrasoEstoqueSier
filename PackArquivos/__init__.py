import secrets
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()

tokenForms = secrets.token_hex(16)
app.config['SECRET_KEY'] = tokenForms
if os.getenv('CONECTOR'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('CONECTOR')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atraso.db'


db = SQLAlchemy(app)
from PackArquivos import routes
