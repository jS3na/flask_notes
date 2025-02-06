from flask import Blueprint, jsonify, request, session, redirect, url_for
from models.note import Note
from models import db

note_bp = Blueprint('note', __name__, template_folder='templates')

@note_bp.route('/', methods=['GET'])
def get():
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({"error": "Sem usuário logado"}), 401
    
    user_notes = Note.get_user_notes(user_id)
    notes_list = [note.serializer() for note in user_notes]
    
    return jsonify({'notes': notes_list})

@note_bp.route('/<note_id>', methods=['GET'])
def get_note(note_id):
    note = Note.query.filter_by(id=note_id).first()
    
    if note is None or note.user_id != session.get('user_id'):
        return jsonify({"error": "Nota não encontrada"}), 404

    return jsonify({'note': note.serializer()})

@note_bp.route('/add', methods=['POST'])
def add():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    
    if not title or not description:
        return jsonify({"error": "Título e descrição são obrigatórios"}), 400

    note = Note(title=title, description=description, user_id=session.get('user_id'))
    db.session.add(note)
    db.session.commit()
    
    return jsonify({"success": True, "note": note.serializer()})

@note_bp.route('/edit/<note_id>', methods=['PUT'])
def edit(note_id):
    note = Note.query.filter_by(id=note_id).first()
    if note is None:
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
