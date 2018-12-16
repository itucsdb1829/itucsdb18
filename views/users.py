from flask_restful import reqparse, Resource
from models.users import Users
from views.auth import auth


class UsersAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('surname', type=str)
        self.parser.add_argument('email', type=str)
        self.parser.add_argument('phone_number', type=str)
        self.parser.add_argument('password', type=str)
        self.parser.add_argument('role', type=str)
        self.parser.add_argument('iban', type=str)

    def get(self, id):
        u = Users.get(id=id)
        if u:
            return u.__dict__
        return {}, 404

    def put(self, id):
        args = self.parser.parse_args()
        u = Users.get(id=id)
        if u and args:
            u.update(**args)
            if args.get('password'):
                u.set_password(args.get('password'))
            return u.__dict__
        return {}, 404

    def delete(self, id):
        u = Users.get(id=id)
        if u:
            r = u.__dict__
            u.delete()
            return r, 200


class UserListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('surname', type=str)
        self.parser.add_argument('email', type=str)
        self.parser.add_argument('phone_number', type=str)
        self.parser.add_argument('password', type=str)
        self.parser.add_argument('role', type=str)
        self.parser.add_argument('iban', type=str)

    def get(self):
        qs = Users.filter()
        if qs:
            r = [u.__dict__ for u in qs]
            return r, 200
        return {}, 404

    def post(self):
        args = self.parser.parse_args()
        if args:
            u = Users.create(**args)
            if u:
                return u.__dict__
        return {}, 404
