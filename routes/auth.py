from flask import Blueprint, make_response, request, session, jsonify
from models.user import User
from models import db
import jwt
import datetime
from functools import wraps
from config import ApplicationConfig

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    name = data.get('name')
    password = data.get('password')
    
    user = User.query.filter_by(name=name).first()

    if user and user.check_password(password):
        token = jwt.encode({
            "user_id": user.id,
            "user_name": name,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, ApplicationConfig.SECRET_KEY)
        
        return jsonify({
            "success": True,
            "token": token
        })
    
    return jsonify({"error": "Credenciais Inválidas"}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    password = data.get('password')

    if not name or not password:
        return jsonify({"error": "Nome e senha são obrigatórios"}), 400

    existing_user = User.query.filter_by(name=name).first()
    if existing_user:
        return jsonify({"error": "Usuário já existe"}), 400
        
    user = User(name=name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        "success": True
    })

@auth_bp.route('/logout')
def logout():
    response = make_response(jsonify({"message": "Logout successful"}))
    response.delete_cookie("token")
    session.clear()
    return response
