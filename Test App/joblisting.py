from App.database import db

class JobListing(db.Model):
    jobID = db.Column(db.String(10), primary_key = True)
    jobName = db.Column(db.String(120), nullable = False)
    recruiterID = db.Column(db.String(10), db.ForeignKey('recruiters.recruiterID'), nullable = False)
    jobField = db.Column(db.String(120), nullable = False)
    jobDescription = db.Column(db.String, nullable = False)
    jobRequirements = db.Column(db.String, nullable = False)
    submissionDeadline = db.Column(db.Date, nullable = False)
    applicants = db.relationship('Application', backref='job_listing', lazy = True)
    applications = db.relationship('Application', backref='job_listing', lazy=True)


    def to_json(self):
        return {

            "jobID": self.jobID,
            "jobName": self.jobName,
            "recruiterID": self.recruiterID,
            "jobField": self.jobField,
            "jobDescription": self.jobDescription,
            "jobRequirements": self.jobRequirements,
            "submissionDeadline": self.submissionDeadline.isoformat(),
            "applications": [application.to_json() for application in self.applications]
            }