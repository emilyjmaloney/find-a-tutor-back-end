from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
    class UserAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.Boolean(), unique=True, nullable=False)
    first_name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    zipcode = db.Column(db.Integer(120), unique=False, nullable=False)

# I dont get
    def __repr__(self):
        return '<UserAccount %r>' % self.username

# I kinda get
    def serialize(self):
        return {
            "id": self.id,
            "user_type": self.user_type,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "zipcode": self.zipcode
        }

class UserProfile(db.Model):
    first_name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    zipcode = db.Column(db.Integer(120), unique=False, nullable=False)
    online = db.Column(db.Boolean(), unique=False, nullable=False)
    profile_image = db.Column(db.String(500), unique=False, nullable=False)
    about_me = db.Column(db.String(1000), unique=False, nullable=False)
    subjects_needed = db.Column(db.String(120), unique=False, nullable=False)
    subjects_tutored = db.Column(db.String(120), unique=False, nullable=False)
    current_grade = db.Column(db.String(120), unique=False, nullable=False)
    wkly_hrs_needed = db.Column(db.String(120), unique=False, nullable=False)
    grades_tutored = db.Column(db.String(120), unique=False, nullable=False)
    subjects_tutored = db.Column(db.String(120), unique=False, nullable=False)

# I dont get
    def __repr__(self):
        return '<UserAccount %r>' % self.username

# I kinda get
    def serialize(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "zipcode": self.zipcode,
            "online": self.online,
            "email": self.email,
            "profile_image": self.profile_image,
            "subjects_needed": self.subjects_needed,
            "subjects_tutored": self.subjects_tutored,
            "current_grade": self.current_grade,
            "wkly_hrs_needed": self.wkly_hrs_needed,
            "grades_tutored": self.grades_tutored,
            "subjects_tutored": self.subjects_tutored
        }
