from flask import Blueprint, make_response, redirect, request, session, url_for, jsonify
from models.user import User
from models import db
import jwt
import datetime
from config import ApplicationConfig

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    name = data.get('name')
    password = data.get('password')
    
    user = User.query.filter_by(name=name).first()

    if user and user.check_password(password):
        response = make_response(jsonify({
            "user_id": user.id,
            "user_name": name
        }))
        
        session["user_id"] = user.id
        
        return response
    
    return jsonify({"error": "Credenciais inválidas"}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    password = data.get('password')

    if not name or not password:
        return jsonify({"message": "Nome e senha são obrigatórios"}), 400

    existing_user = User.query.filter_by(name=name).first()
    if existing_user:
        return jsonify({"message": "Usuário já existe"}), 400
        
    user = User(name=name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    session['user_id'] = user.id
    
    return jsonify({
        "user_id": user.id,
        "user_name": user.name
    })

@auth_bp.route('/logout')
def logout():
    response = make_response(jsonify({"message": "Logout successful"}))
    response.set_cookie('session_token', '', max_age=0)
    response.set_cookie('session', '', max_age=0)
    return response
