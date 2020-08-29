from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# server is running automatically. $ "pipenv run start" to restart the server
#use $ "pipenv run migrate" & "pipenv run upgrade" everytime 

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student = db.Column(db.Boolean, nullable=False, default=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email_address = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    is_active = db.Column(db.Boolean, unique=False, nullable=False)
    sent_messages = db.relationship("Message", backref="sender", foreign_keys="Message.sender_id")
    received_messages = db.relationship("Message", backref="recipient", foreign_keys="Message.recipient_id")
    
    # userprofile=db.relationship("userprofile", backref="author")
    # student=db.relationship("student", backref="author")
    # tutor=db.relationship("tutor", backref="author")
    # sent_messages=db.relationship("Message", backref="sender")
    # received_messages=db.relationship("Message", backref="recipient")

    def __init__(self, student, first_name, last_name, username, email_address, password):
        self.student = student
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email_address = email_address
        self.password = password
        self.is_active = True

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "name": f"{self.first_name} {self.last_name}",
            "id": self.id,
            "student": self.student,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email_address": self.email_address,
            "is_active": self.is_active,
        }


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    profile_image = db.Column(db.String(50), nullable=False)
    about_me = db.Column(db.String(50), nullable=False)
    subjects = db.Column(db.String(50), nullable=False)
    weekday = db.Column(db.String(10), nullable=False)
    daily_timeslot = db.Column(db.String(20), nullable=False)
    online = db.Column(db.String(20), nullable=False)
    zipcode = db.Column(db.Integer, nullable=True)

        
    def __init__(self, user_id, profile_image, about_me, online, subjects, weekday, daily_timeslot, zipcode):
        self.user_id = user_id
        self.profile_image = profile_image
        self.about_me = about_me
        self.subjects = subjects
        self.weekday = weekday
        self.daily_timeslot = daily_timeslot
        self.online = online
        self.zipcode = zipcode
            
    def __repr__(self):
        return f"<UserProfile {self.id}>"
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "profile_image": self.profile_image,
            "about_me": self.about_me,
            "subjects": self.subjects,
            "weekday": self.weekday,
            "daily_timeslot": self.daily_timeslot,
            "online": self.online,
            "zipcode": self.zipcode,
        }

class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    grade = db.Column(db.String(50), nullable=False)
    
    def __init__(self, id, user_id, grade):
        self.user_id = user_id
        self.experience = experience
    
    def __repr__(self):
        return f"<Student {self.id}>"
    
    def serialize(self):
        return{
            "id": self.id,
            "user_id":self.user_id,
            "grade":self.grade
        }


class Tutor(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    experience = db.Column(db.String(250), nullable=False)
    
    def __init__(self, user_id, experience):
        self.user_id = user_id
        self.experience = experience
    
    def __repr__(self):
        return f"<Tutor {self.id}>"
    
    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "experience": self.experience
        }


class Message(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    recipient_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    text = db.Column(db.String(250))
    created_at = db.Column(db.DateTime())
    
    def __init__(self, sender_id, recipient_id, text, created_at):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.text = text
        self.created_at = datetime.now()
    
    def __repr__(self):
        return f"<Message {self.id}>"
    
    def serialize(self):
        return{
            "id": self.id,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "text": self.text,
            "created_at": self.created_at.strftime("%d/%m/%y")
        }

















# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

#     def __init__(self, email, password):
#         self.email = email
#         self.password = password
#         self.is_active = True

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # "is_active": self.is_active
#             # do not serialize the password, its a security breach
#         }
    
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_type = db.Column(db.Boolean(), unique=True, nullable=False)
#     first_name = db.Column(db.String(120), unique=False, nullable=False)
#     last_name = db.Column(db.String(120), unique=False, nullable=False)
#     email = db.Column(db.String(120), unique=False, nullable=False)
#     username = db.Column(db.String(120), unique=False, nullable=False)
#     password = db.Column(db.String(120), unique=False, nullable=False)
#     zipcode = db.Column(db.Integer, unique=False, nullable=False)
#     online = db.Column(db.boolean, unique=False, nullable=False)

# # I dont get
#     def __repr__(self):
#         return '<UserAccount %r>' % self.username

# # I kinda get
#     def serialize(self):
#         return {
#             "id": self.id,
#             "user_type": self.user_type,
#             "first_name": self.first_name,
#             "last_name": self.last_name,
#             "email": self.email,
#             "username": self.username,
#             "password": self.password,
#             "zipcode": self.zipcode
#         }

# class UserProfile(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(120), unique=False, nullable=False)
#     last_name = db.Column(db.String(120), unique=False, nullable=False)
#     zipcode = db.Column(db.Integer, unique=False, nullable=False)
#     online = db.Column(db.Boolean(), unique=False, nullable=False)
#     profile_image = db.Column(db.String(500), unique=False, nullable=False)
#     about_me = db.Column(db.String(1000), unique=False, nullable=False)
#     subjects_needed = db.Column(db.String(120), unique=False, nullable=False)
#     subjects_tutored = db.Column(db.String(120), unique=False, nullable=False)
#     current_grade = db.Column(db.String(120), unique=False, nullable=False)
#     wkly_hrs_needed = db.Column(db.String(120), unique=False, nullable=False)
#     grades_tutored = db.Column(db.String(120), unique=False, nullable=False)
#     subjects_tutored = db.Column(db.String(120), unique=False, nullable=False)

# # I dont get
#     def __repr__(self):
#         return '<UserAccount %r>' % self.username

# # I kinda get
#     def serialize(self):
#         return {
#             "first_name": self.first_name,
#             "last_name": self.last_name,
#             "zipcode": self.zipcode,
#             "online": self.online,
#             "email": self.email,
#             "profile_image": self.profile_image,
#             "subjects_needed": self.subjects_needed,
#             "subjects_tutored": self.subjects_tutored,
#             "current_grade": self.current_grade,
#             "wkly_hrs_needed": self.wkly_hrs_needed,
#             "grades_tutored": self.grades_tutored,
#             "subjects_tutored": self.subjects_tutored
#         }
