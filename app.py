from flask import Flask

from flask import Flask, redirect, render_template, request, url_for, session
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

from models import db, note, user

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_default_key")
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return 'home'

if __name__ == '__main__':
    app.run(debug=True, port=8000)