from sqlite3 import IntegrityError
import applicant as Applicant
import recruiter as Recruiter
import joblisting as JobListing
from App.database import db, get_migrate
from datetime import datetime
import uuid
import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

class Application(db.Model):
    applicationID = db.Column(db.String(10), primary_key = True)
    applicantID = db.Column(db.String(10), db.ForeignKey('applicants.applicantID'), nullable = False)
    jobID = db.Column(db.String(10), db.ForeignKey('job_listings.jobID'), nullable = False)
    applicationStatus = db.Column(db.String(80), default ="Pending", nullable = False)
    submissionDate = db.Column(db.Date, default=datetime.utcnow, nullable = False)


    def to_json(self):
        return {

            "applicationID": self.applicationID,
            "applicantID": self.applicantID,
            "jobID": self.jobID,
            "applicationStatus": self.applicationStatus,
            "submissionDate": self.submissionDate.isoformat()

        }

    def create_user (userID, username, password,email, role):
        
        if role == 'applicant':
            user = Applicant (username = username, password = password, email = email , userID = userID)
        
        elif role == 'recruiter':
            user = Recruiter (username = username, password = password, email = email, userID = userID)
        
        try:
            db.session.add(user)
            db.session.commit()
        
        except IntegrityError as e:
            db.session.rollback()

            print ("Email is already in use.")
        
        else:
            print (user)


    def get_all_users():
        return Applicant.User.query.all()

    def get_all_users_json():
        return [user.to_json() for user in Applicant.User.query.all()]


    def create_job_listing(jobID, jobName, recruiterID, jobField, jobDescription, jobRequirements, submissionDeadline):

        job = JobListing(
            jobID = str(uuid.uuid4()),
            jobName=jobName,
            recruiterID=recruiterID,
            jobField=jobField,
            jobDescription=jobDescription,
            jobRequirements=jobRequirements,
            submissionDeadline=submissionDeadline
        )
        db.session.add(job)
        db.session.commit()

        return job.to_json()


    def get_job_listing(jobID):
        job = JobListing.query.get(jobID)
        if job:
            return job.to_json()
        return None

    def get_all_job_listings_json():
        jobs = JobListing.query.all()
        return [job.to_json() for job in jobs]

# Application functions
    def apply_to_job(applicantID, jobID, coverPageDetails, resumeDetails):
        job = JobListing.query.get(jobID)
        if not job:
            return {"error": "Job listing not found"}
        
        application = Application(
            applicationID= str(uuid.uuid4()),
            applicantID=applicantID,
            jobID=jobID,
            applicationStatus= "Pending",
            submissionDate = datetime.utcnow()
        )

        db.session.add(application)
        db.session.commit()
        return application.to_json()

    def get_applications_for_job(jobID):
        applications = Application.query.filter_by(jobID = jobID).all()
        return [application.to_json() for application in applications]

    def get_applications_for_applicant(applicantID):
        applications = Application.query.filter_by(applicantID = applicantID).all()
        return [application.to_json() for application in applications]

    def initialize():
        db.drop_all()
        db.create_all()
