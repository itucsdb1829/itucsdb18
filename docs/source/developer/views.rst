Views
=====

The project has views that receives request end creates response with REST standards. Endpoints
of the API is described in server.js.

.. code-block:: python

    #server.js
    api.add_resource(TokenToUserAPI, '/me')
    api.add_resource(AuthAPI, '/auth')

    api.add_resource(UsersAPI, '/users/<int:id>')
    api.add_resource(UserListAPI, '/users')

    api.add_resource(QuestionsAPI, '/questions/<int:id>')
    api.add_resource(QuestionListAPI, '/questions')

    api.add_resource(FeedbacksAPI, '/feedbacks/<int:id>')
    api.add_resource(FeedbackListAPI, '/feedbacks')

**Auth View**

Server side of the Question Collector is protected by token based authentication. To get token,
client should make a post request to */auth* endpoint with a body includes email and password.

.. code-block:: python

    #views/auth.py
    class AuthAPI(Resource):
        def __init__(self):
            self.parser = reqparse.RequestParser()
            self.parser.add_argument('username', type=str, help='user e-mail')
            self.parser.add_argument('password', type=str, help='user password')

        def post(self):
            args = self.parser.parse_args()
            email = args.get('username')
            password = args.get('password')
            if email and password:
                u = Users.get(email=email)
                if u and u.check_password(password):
                    return {'token': token_serializer.dumps({'email': email,
                                                             'role': u.role}).decode('utf-8'),
                            'role': u.role}, 201



This API firstly parses the username and passwords arguments of the request body. After that
it finds the user and checks the encrypted password. If password is correct it created a token
and sends to client.


**Model Views**

As an example of a Model View, source code of the user model's view is given below,

.. code-block:: python

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


UsersAPI is working on */users/<id>* endpoint and it supports **GET, PUT and DELETE** operations
with REST standards.

UserListAPI is working on */users* endpoint and it supports **GET and POST** operations
with REST standards. It returns all of the user list with GET request and creates a new
user with POST request.