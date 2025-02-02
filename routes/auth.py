from flask import Blueprint, redirect, render_template, request, session, url_for
from models.user import User
from models import db

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user = User.query.filter_by(name=name).first()

        if user and user.check_password(password):
            session['user'] = name
            session['user_id'] = user.id
            session['token'] = 'teste'
            return redirect(url_for('note.root'))

    return render_template('login.html')

@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method ==  'POST':
        name = request.form['name']
        password = request.form['password']
        
        user = User(name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.before_request
@auth_bp.before_request
def check_logged():
    
    if request.endpoint in ['auth.logout']:
        return
    
    if 'token' in session:
        return redirect(url_for('user.notes'))
