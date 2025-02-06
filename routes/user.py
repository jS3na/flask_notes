from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for

from models.user import User

user_bp = Blueprint('user', __name__, template_folder='templates')

@user_bp.route('/@me')
def get_current_user():
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({"error": "Sem usuário logado"}), 401
    
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        'user_id': user.id,
        'user_name': user.name
    })
    
@user_bp.route('/is_authenticated')
def is_authenticated():
    if 'user_id' in session:
        return jsonify({"authenticated": True, "user_id": session["user_id"]})
    return jsonify({"authenticated": False})
