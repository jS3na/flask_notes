from flask import Blueprint, make_response, request, session, jsonify
from models.user import User
from models import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    name = data.get('name')
    password = data.get('password')
    
    user = User.query.filter_by(name=name).first()

    if user and user.check_password(password):
        session["user_id"] = user.id
        return jsonify({
            "user_id": user.id,
            "user_name": name,
            "redirect": "/home"
        })
    
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
    session.clear()
    return jsonify({"message": "Logout successful"})
