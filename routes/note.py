from flask import Blueprint, jsonify, request
from models.note import Note
from models import db
from utils import jwt_decode
from functools import wraps

note_bp = Blueprint('note', __name__, template_folder='templates')

def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return jsonify({"error": "Sem token fornecido"}), 401
        
        decoded_token = jwt_decode(token)
        if "error" in decoded_token:
            return jsonify({"error": decoded_token["error"]}), 401
        
        user_id = decoded_token.get("user_id")
        if not user_id:
            return jsonify({"error": "Sem usuário logado"}), 401
        
        request.user_id = user_id
        return f(*args, **kwargs)
    
    return decorated_function

@note_bp.route('/', methods=['GET'])
@authenticate
def get():
    user_notes = Note.get_user_notes(request.user_id)
    notes_list = [note.serializer() for note in user_notes]
    return jsonify({'notes': notes_list})

@note_bp.route('/<note_id>', methods=['GET'])
@authenticate
def get_note(note_id):
    note = Note.query.filter_by(id=note_id).first()
    if note is None or note.user_id != request.user_id:
        return jsonify({"error": "Nota não encontrada"}), 404
    return jsonify({'note': note.serializer()})

@note_bp.route('/add', methods=['POST'])
@authenticate
def add():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    
    if not title or not description:
        return jsonify({"error": "Título e descrição são obrigatórios"}), 400

    note = Note(title=title, description=description, user_id=request.user_id)
    db.session.add(note)
    db.session.commit()
    
    return jsonify({"success": True, "note": note.serializer()})

@note_bp.route('/edit/<note_id>', methods=['PUT'])
@authenticate
def edit(note_id):
    note = Note.query.filter_by(id=note_id).first()
    if note is None or note.user_id != request.user_id:
        return jsonify({"error": "Nota não encontrada"}), 404

    data = request.json
    title = data.get('title')
    description = data.get('description')

    if not title or not description:
        return jsonify({"error": "Título e descrição são obrigatórios"}), 400

    note.title = title
    note.description = description
    db.session.commit()
    
    return jsonify({"success": True, "note": note.serializer()})
