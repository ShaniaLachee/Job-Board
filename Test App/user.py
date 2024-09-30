from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    userID = db.Column(db.String (10), primary_key = True, extend_existing=True)
    username = db.Column(db.String(80), nullable = False)
    password = db.Column (db.String(120), nullable = False)
    email = db.Column (db.String (120), nullable = False, unique = True)
    role = db.Column (db.String, nullable = False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    __mapper_args__ = {
    "polymorphic_identity": "user",
    "polymorphic_on" : role
}

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    

    def to_json(self):
        return{
            "userID" : self.userID,
            "username" : self.username,
            "email" : self.email,
            "role" : self.role
        }

    def __repr__ (self):
        return f'<User {self.username} - {self.role}>'


