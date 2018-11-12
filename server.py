import os

from flask import Flask, request, Response

from models.users import Users

app = Flask(__name__)


# u = Users(name='sedat', surname='cagdas', email='sedat@test.com', role='admin', password='pw')
# u.create()
print('heloo')


def test_method(name, surname, email, role, password):
    print(name, surname, role, email, password)


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
    app.run()
