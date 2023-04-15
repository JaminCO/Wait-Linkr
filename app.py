from flask import Flask, request
import json
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'

db = SQLAlchemy(app)

# Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(500), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    company = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120), nullable=False)
    joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Waitlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    waitlist_name = db.Column(db.String(20), unique=True, nullable=False)
    user = db.ForeignKey('User', related_name='creator', on_delete=db.CASCADE)
    company = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class WaitlistUsr(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    waitlist = db.ForeignKey('Waitlist', related_name='waitlist', on_delete=db.CASCADE)
    firstname = db.Column(db.String(20), unique=True, nullable=False)
    lastname = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    message = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

waitlist = {
    0:{
            "firstname":"Jamin",
            "lastname":"Onuegbu",
            "email":"jtechlab2007@gmail.com",
            "message":"test test",
        }
}


@app.route("/")
def home():
    return """
    <h1> Waitlist </h1>
    <h3>Add Email</h3>
    """

@app.route("/add", methods=["GET","POST"])
def add_email():
    # print(request.args.get("email"))
    data = request.get_json()

    email = data["email"]
    firstname = data["firstname"]
    lastname = data["lastname"]

    waitlist = WaitlistUsr(firstname=firstname, lastname=lastname, email=email)
    db.session.add(waitlist)
    db.session.commit()
    # keys = []
    # for i in waitlist:
        # keys.append(i)
    # last_key = keys[-1]
    # new_key = last_key+1
    # temp_dict = {
    #     "firstname":firstname,
    #     "lastname":lastname,
    #     "email":email,
    # }
    # waitlist[new_key] = temp_dict
    return json.dumps({"message":"success"})


@app.route("/list")
def list():
    waitlist = WaitlistUsr.query.all()
    list = []
    lists = {}
    for i in waitlist:
        data = {}
        data['firstname'] = i.firstname
        data['lastname'] = i.lastname
        data['email'] = i.email
        lists[i.email] = data
    return json.dumps(lists)


if "__main__" == __name__:
    db.create_all()
    app.run(debug=True)
