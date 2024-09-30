from sqlite3 import IntegrityError
import uuid
import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup
from datetime import datetime
import joblisting as JobListing
import application as Application
from database import db, get_migrate
# from App.models import User
from main import create_app
from controllers import ( create_user, get_all_users_json, get_all_users, initialize )
# from App.models import db, User, Applicant, Recruiter, JobListing, Application


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


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username")
@click.argument("password")
@click.argument("email")
@click.argument ("role")

def create_user_command(username, password,email,role):
    create_user(username, password,email,role)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Job Commands
'''

job_cli = AppGroup('job', help='Job Listing commands')

@job_cli.command("create", help="Creates a job listing")
@click.argument("job_name")
@click.argument("recruiter_id")
@click.argument("job_field")
@click.argument("job_description")
@click.argument("job_requirements")
@click.argument("submission_deadline")  

def create_job_command(job_name, recruiter_id, job_field, job_description, job_requirements, submission_deadline):
    job = create_job_listing(
        jobName=job_name,
        recruiterID=recruiter_id,
        jobField=job_field,
        jobDescription=job_description,
        jobRequirements=job_requirements,
        submissionDeadline=datetime.strptime(submission_deadline, '%d-%m-%Y')
    )

    print(f'Job "{job_name}" created by recruiter {recruiter_id}!')

@job_cli.command("list", help="Lists all job listings")

def list_jobs_command():
    jobs = get_all_job_listings_json()
    for job in jobs:
        print(job)

app.cli.add_command(job_cli)


'''
Application Commands
'''
application_cli = AppGroup('application', help='Job Application commands')

@application_cli.command("apply", help="Applies to a job listing")
@click.argument("applicant_id")
@click.argument("job_id")
@click.argument("cover_page_details")
@click.argument("resume_details")

def apply_job_command(applicant_id, job_id, cover_page_details, resume_details):
    application = apply_to_job(
        applicantID=applicant_id,
        jobID=job_id,
        coverPageDetails=cover_page_details,
        resumeDetails=resume_details
    )
    print(f'Applicant {applicant_id} applied to job {job_id}!')

@application_cli.command("list-for-job", help="Lists all applications for a job")
@click.argument("job_id")

def list_applications_for_job_command(job_id):
    applications = get_applications_for_job(job_id)
    for application in applications:
        print(application)

@application_cli.command("list-for-applicant", help="Lists all applications for an applicant")
@click.argument("applicant_id")

def list_applications_for_applicant_command(applicant_id):
    applications = get_applications_for_applicant(applicant_id)
    for application in applications:
        print(application)

app.cli.add_command(application_cli)


'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)
