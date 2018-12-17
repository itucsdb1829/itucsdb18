import os

from flask import Flask, request, Response
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse

from views.auth import token_serializer, AuthAPI, auth, TokenToUserAPI
from models.users import Users
from views.feedbacks import FeedbackListAPI, FeedbacksAPI
from views.questions import QuestionsAPI, QuestionListAPI
from views.users import UsersAPI, UserListAPI

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)



@auth.verify_token
def verify_token(token):
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

api.add_resource(QuestionsAPI, '/questions/<int:id>')
api.add_resource(QuestionListAPI, '/questions')

api.add_resource(FeedbacksAPI, '/feedbacks/<int:id>')
api.add_resource(FeedbackListAPI, '/feedbacks')

@app.route("/")
def home_page():
    return 'This is api welcome page'

if __name__ == "__main__":
    app.run(debug=True  )
