from flask import Blueprint, jsonify, render_template, redirect, request, session, url_for

from models.note import Note
from models import db

note_bp = Blueprint('note', __name__, template_folder='templates')

@note_bp.route('/', methods=['GET'])
def root():
    user_notes = Note.get_user_notes(session['user_id'])
    notes_list = [note.serializer() for note in user_notes]  # Convertendo cada Note para dicionário
    return jsonify({'notes': notes_list})

@note_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        note = Note(title=title, description=description, user_id=session['user_id'])
        db.session.add(note)
        db.session.commit()
        
        return redirect(url_for('note.root'))
    return render_template('add_note.html')

@note_bp.route('/edit/<note_id>', methods=['GET', 'POST'])
def edit(note_id):
    note = Note.query.filter_by(id=note_id).first()
    
    if note is None:
        return "Nota não encontrada", 404
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        note.title = title
        note.description = description
        
        db.session.commit()
        
        return redirect(url_for('note.root')) 
    
    return render_template('edit_note.html', note=note)
        

@note_bp.before_request
def check_logged():
    if request.endpoint in ['auth.login', 'auth.logout']:
        return

    if 'token' not in session:
        return redirect(url_for('auth.login'))