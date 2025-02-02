from flask import Flask

from routes.user import user_bp
from routes.auth import auth_bp
from routes.note import note_bp

from flask import Flask, redirect, render_template, request, url_for, session
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

from models import db

app = Flask(__name__)
app.secret_key = 'abc123'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return 'home'

@app.before_request
def check_logged():
    if request.endpoint in ['auth.login', 'auth.logout', 'auth.register']:
        return

    if 'token' not in session:
        return redirect(url_for('auth.login'))

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(note_bp, url_prefix='/note')

if __name__ == '__main__':
    app.run(debug=True, port=8000)