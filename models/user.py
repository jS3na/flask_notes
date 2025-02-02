from models import db
from bcrypt import gensalt, hashpw, checkpw

class User(db.Model):

    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(128))

    def set_password(self, password):
        salt = gensalt()
        self.password = hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        return checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def serializer(self):
        return {
            'id': self.id,
            'name': self.name
        }
