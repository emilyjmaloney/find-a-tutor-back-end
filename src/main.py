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
from models import db, User
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
        db.session.add(new_user)
        try:
            db.session.commit()
            return jsonify(new_user.serialize()), 201
        except Exception as error:
            db.session.rollback()
            return jsonify({
                "msg": error.args
            }), 500
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
@app.route('/protected', methods=['GET'])
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
        return jsonify({
            "msg": "Yay! You sent your token correctly so I know who you are!",
            "user_data": specific_user.serialize()
        }), 200
@app.route('/getall', methods=['GET'])
def handle_getall():
    users = User.query.all()
    serialized_users = []
    for user in users:
        serialized_users.append(user.serialize())
    return jsonify(serialized_users), 200

# All Users
# UN: emilyjean.maloney@gmail.com PW: emsmSecret
# UN: emily@gmail.com PW: password123
# UN: emilym@gmail.com PW: password123


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
