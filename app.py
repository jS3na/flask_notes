from routes.user import user_bp
from routes.auth import auth_bp
from routes.note import note_bp

from flask import Flask, redirect, render_template, request, url_for, session
from flask_migrate import Migrate
from flask_cors import CORS
from flask_session import Session

from config import ApplicationConfig

from models import db

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

CORS(app, supports_credentials=True)

server_session = Session(app)

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return 'home'

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(note_bp, url_prefix='/note')

if __name__ == '__main__':
    app.run(debug=True, port=8000)