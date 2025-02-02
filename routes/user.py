from flask import Blueprint, redirect, render_template, request, session, url_for

user_bp = Blueprint('user', __name__, template_folder='templates')

@user_bp.route('/')
def root():
    return '<h1>bem vindo a area do user</h1>'

@user_bp.before_request
def check_logged():
    if request.endpoint in ['auth.login', 'auth.logout']:
        return

    if 'token' not in session:
        return redirect(url_for('auth.login'))