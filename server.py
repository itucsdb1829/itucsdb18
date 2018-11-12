from flask import Flask

from models.users import Users

app = Flask(__name__)


u = Users(name='sedat', surname='cagdas', email='sedat@test.com', role='admin', password='pw')
u.create()
print('heloo')



@app.route("/")
def home_page():
    return 'sa'


if __name__ == "__main__":
    app.run()
