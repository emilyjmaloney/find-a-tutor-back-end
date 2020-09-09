"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Message, UserProfile, Student, Tutor
from flask_jwt_simple import JWTManager, create_jwt, get_jwt_identity, jwt_required #added to match the newly added endponts for new user and login
#from models import Person
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# jwt_simple config
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code
# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200
@app.route('/signup', methods=['POST'])     #not from website, Ernesto created, doesn't use jwt to create users
def handle_signup():
    input_data = request.json
    if (
        "student" in input_data and
        "first_name" in input_data and
        "last_name" in input_data and
        "username" in input_data and
        'email_address' in input_data and 
        'password' in input_data
    ):
        new_user = User(
            input_data["student"],
            input_data["first_name"],
            input_data["last_name"],
            input_data["username"],
            input_data["email_address"],
            input_data["password"],
            )
        #
        db.session.add(new_user)
        try:
            db.session.commit()
            new_userprofile = UserProfile(
              user_id = new_user.id,
              about_me = "I am happy",
              profile_image = None,
              subjects = None,
              weekday = None,
              daily_timeslot = None,
              online = None,
              zipcode = None
            )
            db.session.add(new_userprofile)
            db.session.commit()
            if new_user.student == True:
                new_userrole = Student(
                    user_id = new_user.id,
                    grade = None
                )
            else:
                new_userrole = Tutor(
                    user_id = new_user.id,
                    experience = None
                )
            db.session.add(new_userrole)
            db.session.commit()
            return jsonify(new_user.serialize()), 201
        except Exception as error:
            db.session.rollback()
            return jsonify({
                "msg": error.args
            }), 500
        # user1 = User.query.get(new_user.id)
        
    else:
        return jsonify({
            "msg": "check your keys..."
        }), 400
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    params = request.json
    email = params.get('email', None)
    password = params.get('password', None)
    if not email:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    specific_user = User.query.filter_by(
        email_address=email
    ).one_or_none()
    if isinstance(specific_user, User):
        if specific_user.password == password:
            # oh, this person is who it claims to be!
            # Identity can be any data that is json serializable
            response = {'jwt': create_jwt(identity=specific_user.id), "user": specific_user.serialize()}
            return jsonify(response), 200
        else:
            return jsonify({
            "msg": "bad credentials"
        }), 400
    else:
        return jsonify({
            "msg": "bad credentials"
        }), 400
    # if username != 'test' or password != 'test':
    #     return jsonify({"msg": "Bad username or password"}), 401
@app.route('/get-single-user', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    specific_user_id = get_jwt_identity()
    specific_user = User.query.filter_by(
        id=specific_user_id
    ).one_or_none()
    # specific_user = User.query.get(specific_user_id)
    if specific_user is None:
        return jsonify({
            "msg": "user not found"
        }), 404
    else:
        return jsonify(
            specific_user.serialize()
        ), 200
@app.route('/getall', methods=['GET'])
def handle_getall():
    users = User.query.all()
    serialized_users = []
    for user in users:
        serialized_users.append(user.serialize())
    return jsonify(serialized_users), 200
@app.route('/messages', methods=['POST'])
@jwt_required
def messages():
    # First we get the payload json
    body = request.get_json()
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'text' not in body:
        raise APIException('You need to specify the text', status_code=400)
    if 'created_at' not in body:
        raise APIException('You need to specify the created at', status_code=400)
    if 'recipient_id' not in body:
        raise APIException('You need to specify the recipient id', status_code=400)
    # at this point, all data has been validated, we can proceed to inster into the bd
    user1 = Message(text=body['text'], created_at=body['created_at'], recipient_id=body['recipient_id'], sender_id=get_jwt_identity())
    db.session.add(user1)
    db.session.commit()
    return "ok", 200
@app.route('/user-profile', methods=['GET'])
def handle_profile():
    """
    Create person and retrieve all persons
    """
    # GET request
    all_people = UserProfile.query.all()
    all_people = list(map(lambda x: x.serialize(), all_people))
    return jsonify(all_people), 200
@app.route('/update-student/<int:id>', methods=["PATCH"])
def update_student(id):
    body = request.get_json()
    student = Student.query.get(id)
    print(student)
    if body is None:
        raise APIException('Student not found', status_code=404)    
    if "grade" in body:
        student.grade = body["grade"]
    db.session.commit()
    return jsonify(student.serialize()), 200
@app.route('/update-tutor/<int:id>', methods=["PATCH"])
def update_tutor(id):
    body = request.get_json()
    tutor = Tutor.query.get(id)
    if body is None:
        raise APIException('Tutor not found', status_code=404)    
    if "experience" in body:
        tutor.experience = body["experience"]
    db.session.commit()
    return jsonify(tutor.serialize()), 200
@app.route('/update-userprofile/<int:id>', methods=["PATCH"])
def update_user_profile(id):
    body = request.get_json()
    user_profile = UserProfile.query.get(id)
    if body is None:
        raise APIException('User_profile not found', status_code=404)    
    if "profile_image" in body:
        user_profile.profile_image = body["profile_image"]
    if "about_me" in body:
        user_profile.about_me = body["about_me"]
    if "subjects" in body:
        user_profile.subjects = body["subjects"]
    if "weekday" in body:
        user_profile.weekday = body["weekday"]
    if "daily_timeslot" in body:
        user_profile.daily_timeslot = body["daily_timeslot"]
    if "online" in body:
        user_profile.online = body["online"]
    if "zipcode" in body:
        user_profile.zipcode = body["zipcode"]
    db.session.commit()
    return jsonify(user_profile.serialize()), 200

@app.route('/update/<int:id>', methods=["PATCH"])
def update_user(id):
    body = request.get_json()
    user_profile = User_profile.query.get(id)
    if body is None:
        raise APIException('User_profile not found', status_code=404)    
    if "student" in body:
        user.student = body["student"]
    if "first_name" in body:
        user.first_name = body["first_name"]
    if "last_name" in body:
        user.last_name = body["last_name"]
    if "email_address" in body:
        user.email_address = body["email_address"]
    if "username" in body:
        user.username = body["username"]
    db.session.commit()
    return jsonify(user.serialize()), 200

@app.route('/search', methods=["GET"])
def search_user ():
    search_dictionary = request.args.to_dict()
    print(search_dictionary)
    if "student" in search_dictionary:
        online_user_profiles = UserProfile.query.filter_by(online="option3").all()
        bi_user_profiles = UserProfile.query.filter_by(online="option1").all()
        in_person_user_profiles = UserProfile.query.filter_by(online="option2").all()
        profiles_by_online = []
        if search_dictionary["radio"] == "option1":
            profiles_by_online = [ *online_user_profiles, *bi_user_profiles, *in_person_user_profiles ]
        elif search_dictionary["radio"] == "option2":
            profiles_by_online = [ *bi_user_profiles, *in_person_user_profiles ]
        else:
            profiles_by_online = [ *online_user_profiles, *bi_user_profiles ]
        
        if search_dictionary["student"] == True:
            #search for tutors in the tutor table
            tutors = list(filter(lambda profile: not profile.is_student, profiles_by_online))
            if "zipcode" in search_dictionary and search_dictionary["zipcode"] !="":
                filtered_tutors = list(filter(lambda tutor: search_dictionary["zipcode"] in tutor.zipcode, tutors))
            else:
                filtered_tutors=[*tutors]
            serialize_tutors = []
            for tutor in list(filter(lambda tutor: search_dictionary["subject"] in tutor.subjects, filtered_tutors)):
                serialize_tutors.append(tutor.serialize())
            return jsonify(serialize_tutors), 200
        else:
            #search for students in the student table
            students = list(filter(lambda profile: profile.is_student, profiles_by_online))
            
            if "zipcode" in search_dictionary and search_dictionary["zipcode"] !="":
                filtered_students = list(filter(lambda student: search_dictionary["zipcode"] in student.zipcode, students))
            else:
                filtered_students =[*students]
            if "grade" in search_dictionary and search_dictionary["grade"] !="":
                results = list(filter(lambda student:
                    student.get_grade()==search_dictionary["grade"], filtered_students))
            else:
                results=[*filtered_students]
            serialize_students = []
            for student in list(filter(lambda student: search_dictionary["subject"] in student.subjects, results)):
                serialize_students.append(student.serialize())
            return jsonify(serialize_students), 200
    return 400

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
