from flask import Flask, request, jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
# from flask_login import UserMixin

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'

db = SQLAlchemy(app)

app.app_context().push()

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
    waitlists = db.relationship('Waitlist', backref='creator', lazy=True)
    joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Waitlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    waitlist_name = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    waiter = db.relationship('Waiter', backref='waitlist', lazy=True)
    company = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Waiter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    waitlist_id = db.Column(db.Integer, db.ForeignKey('waitlist.id'), nullable=False)
    username = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    message = db.Column(db.Text)
    joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


# Landing Page
@app.route("/")
def home():
    return """
    <h1> Waity </h1>
    """

# Sign Up

# Sign in

# Dashboard

# List of waiters

# Create api url/id

# Launch

# Add new waiter

# Update user (admin)

# Delete waiter

# Send emails

# Launch email

# Delete account 


@app.route("/add1", methods=["GET","POST"])
def add_email_1():
    if request.method == 'POST':
        data = request.form
        email = data["email"]
        print(email)
        firstname = "usr1237"+str(email[0:3])

        waitlist = Waiter(username=username, email=email)
        db.session.add(waitlist)
        db.session.commit()
        return jsonify({"message":"success", "status":1})
    return jsonify({"message":"failed", "status":0})


@app.route("/add", methods=["GET","POST"])
def add_email():
    if request.method == 'POST':
        data = request.get_json()
        email = data["email"]
        print(email)
        firstname = "usr123456787"

        waitlist = Waiter(username=username, email=email)
        db.session.add(waitlist)
        db.session.commit()
        return jsonify({"message":"success", "status":1})
    return jsonify({"message":"failed", "status":0})

@app.route("/list")
def list():
    waitlist = Waiter.query.all()
    list = []
    lists = {}
    for i in waitlist:
        data = {}
        data['username'] = i.username
        data['email'] = i.email
        lists[i.email] = data
    return jsonify(lists)


if "__main__" == __name__:
    db.create_all()
    app.run(debug=True)
