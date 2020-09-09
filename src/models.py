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
    userprofile = db.relationship("UserProfile", uselist=False, backref="user")
    student_profile = db.relationship("Student", uselist=False, backref="user")
    tutor_profile = db.relationship("Tutor", uselist=False, backref="user")

# _________________________________________________________________________________________________________________________________________
# Example of 1 to 1 from docs.sqlalchemy: https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#one-to-one
# class Parent(Base):
#     __tablename__ = 'parent'
#     id = Column(Integer, primary_key=True)
#     child = relationship("Child", uselist=False, back_populates="parent")

# class Child(Base):
#     __tablename__ = 'child'
#     id = Column(Integer, primary_key=True)
#     parent_id = Column(Integer, ForeignKey('parent.id'))
#     parent = relationship("Parent", back_populates="child")  
# _________________________________________________________________________________________________________________________________________

# Example of 1 to Many from flask-sqlalc hemy: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#one-to-many-relationships
# class Person(db.Model):     <--- THIS IS "USER" FOR ME
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     addresses = db.relationship('Address', backref='person', lazy=True)

# class Address(db.Model):     <--- THIS IS "MESSAGE" FOR ME
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), nullable=False)
#     person_id = db.Column(db.Integer, db.ForeignKey('person.id'),     <--- "person_id" IS "user_id" FOR ME
#         nullable=False)
# _________________________________________________________________________________________________________________________________________

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
            "userprofile": self.userprofile.serialize(),
            "student_profile": self.student_profile.serialize() if self.student else None,
            "tutor_profile": self.tutor_profile.serialize() if not self.student else None,
        }


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    profile_image = db.Column(db.String(50), nullable=True)
    about_me = db.Column(db.String(200), nullable=True)
    subjects = db.Column(db.String(50), nullable=True)
    weekday = db.Column(db.String(10), nullable=True)
    daily_timeslot = db.Column(db.String(20), nullable=True)
    online = db.Column(db.String(20), nullable=True)
    zipcode = db.Column(db.Integer, nullable=True)
    
    def load_subjects(self):
        subjects = self.subjects.split(",")
        return subjects
    
    def set_subjects(self, new_subjects):
        self.subjects = ",".join(new_subjects) 
        db.session.commit()

    def get_grade(self):
        user=User.query.get(self.user_id)
        if user.student_profile:
            return str(user.student_profile.grade)
        return None

    def is_student(self):
        user = User.query.get(self.user_id)
        print(f"user profile check {user.student_profile}")
        return True if user.student_profile else False

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
    grade = db.Column(db.String(50), nullable=True)

    def __init__(self, user_id, grade):
        self.user_id = user_id
        self.grade = grade
    
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
    experience = db.Column(db.String(200), nullable=True)

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


