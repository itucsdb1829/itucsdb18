import os

from flask import Flask, request, Response
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse

from views.auth import token_serializer, AuthAPI, auth, TokenToUserAPI
from models.users import Users
from views.users import UsersAPI, UserListAPI

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)



@auth.verify_token
def verify_token(token):
    print(token)
    try:
        data = token_serializer.loads(token)
    except:
        return False
    if 'email' in data:
        return True
    return False


api.add_resource(TokenToUserAPI, '/me')
api.add_resource(AuthAPI, '/auth')
api.add_resource(UsersAPI, '/users/<int:id>')
api.add_resource(UserListAPI, '/users')




@auth.login_required
@app.route("/")
def home_page():
    print(auth.authenticate())
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
