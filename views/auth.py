import os

from flask_restful import reqparse, Resource
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from models.users import Users

auth = HTTPTokenAuth('Bearer')
token_serializer = Serializer(os.getenv("TOP_SECRET_KEY"), expires_in=3600)


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


class TokenToUserAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('token', type=str, help='token')

    def post(self):
        args = self.parser.parse_args()
        token = args.get('token')
        if token:
            try:
                data = token_serializer.loads(token)
            except:
                return {}, 404
            if 'email' in data:
                u = Users.get(email=data['email'])
                if u:
                    return [u.__dict__], 200
            return {}, 404
