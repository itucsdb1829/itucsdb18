import os

from flask import Flask, request, Response
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
from flask_restful import Api, Resource, reqparse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from models.users import Users

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)
token_serializer = Serializer('top_secret_key', expires_in=3600)
auth = HTTPTokenAuth('Bearer')




@auth.verify_token
def verify_token(token):
    g.user = None
    try:
        data = token_serializer.loads(token)
    except:
        return False
    if 'username' in data:
        g.user = data['username']
        return True
    return False


class AuthAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='user e-mail')
        self.parser.add_argument('password', type=str, help='user password')

    def post(self):
        args = self.parser.parse_args()
        print(args)
        email = args.get('username')
        password = args.get('password')
        if email and password:
            u = Users.get(email=email)
            if u and u.check_password(password):
                return {'token': token_serializer.dumps(
                    {'email': email,
                     'role': u.role}).decode('utf-8')}, 201


api.add_resource(AuthAPI, '/auth', endpoint = 'auth')



class UserAPI(Resource):
    decorators = [auth.login_required]

    def get(self, id):
        return {'result': id}, 200

    def put(self, id):
        pass

    def delete(self, id):
        pass


api.add_resource(UserAPI, '/users/<int:id>', endpoint = 'user')


@app.route("/login")
@auth.login_required
def get_token():
    return auth.authenticate_header()

@app.route("/")
def home_page():
    return 'sa'


@app.route("/users/create", methods=['POST'])
def create_user():
    if request.method == 'POST':
        if request.headers.get('Token') != os.getenv('AUTH_TOKEN'):
            return Response(status=401)
        user_data=dict()
        for key, value in request.form.items():
            user_data[key] = value

        u = Users(**user_data)
        u.create()
    return Response(status=201)


if __name__ == "__main__":
    app.run(debug=True  )
