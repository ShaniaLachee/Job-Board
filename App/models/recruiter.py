import user as User
from App.database import db

class Recruiter (User):
    __tablename__ = 'recruiters'
    recruiterID = db.Column (db.String (10), db.ForeignKey ('users.userID'), primary_key = True)
    
    __mapper_args__ = {
        "polymorphic_identity": "recruiter"
    }

    def to_json(self):
        return super().to_json()
