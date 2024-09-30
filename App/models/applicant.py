import user as User
from App.database import db

class Applicant(User):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'applicant'
    applicantID = db.Column (db.String (10), db.ForeignKey ('users.userID'),primary_key = True)
    coverPageDetails = db.Column (db.String, nullable = False)
    resumeDetails = db.Column (db.String, nullable = False)

    applicants = db.relationship ('Application', backref = 'applicant', lazy = True)

    __mapper_args__ = {
        "polymorphic_identity": "applicant",

    }


    def __init__(self, userID, username, password, email, coverPageDetails, resumeDetails):
        super.__init__(username, email, password)
        self.coverPageDetails = coverPageDetails
        self.resumeDetails = resumeDetails

    def to_json(self):
        return super().to_json() | {

            "coverPageDetails": self.coverPageDetails,
            "resumeDetails": self.resumeDetails

        }