from models import db

class Note(db.Model):
    
    __tablename__ = 'notes'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    
    user = db.relationship('User', foreign_keys=[user_id])
    
    @staticmethod
    def get_user_notes(user_id):
        return Note.query.filter_by(user_id=user_id).all()
    
    def serializer(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description
        }
