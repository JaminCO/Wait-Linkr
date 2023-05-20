from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_mail import Mail, Message
from dotenv import load_dotenv
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_bcrypt import Bcrypt


load_dotenv()

mail = Mail()
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = ('Wait-Linkr', 'pythonacademia101@gmail.com')
SQLALCHEMY_TRACK_MODIFICATIONS=True

db = SQLAlchemy(app)
mail.init_app(app)

app.app_context().push()
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=30)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class SigninForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('signin'))
    return render_template('signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')
    return render_template('signin.html', form=form)


class Waiter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    # token = db.Column(db.String(50), unique=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow())

# home/dashboard
@app.route('/')
def home():
    return "THERE IS NOTHING TO SEE HERE, KEEP GOING"

# check if waiter already exists
def check_waiter_exists(email):
    list = Waiter.query.order_by(Waiter.date.desc()).all()
    if len(list) < 1:
        return False
    else:
        # print(list)
        w_list = []
        for i in list:
            if i.email == email:
                w_list.append(True)
            else:
                w_list.append(False)
        print(w_list)
        if True in w_list:
            return True
        else:
            if False in w_list:
                return False


# add waiter
@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        # data = request.get_json()
        # email = data['email']
        # message = data['message']
        # -----------------------------
        email = request.form['email']
        # print(email)
        # message = request.form['message']
        ds = check_waiter_exists(email)
        # print(ds)
        if ds is False:
            new_waiter = Waiter(email=email)
            db.session.add(new_waiter)
            db.session.commit()
            # print("1")
            confirmation(email)
            return jsonify({"msg":f"{email} added to waitlist"})
        elif ds is True:
                # print("2")
                return jsonify({"msg":f"{email} already exists"})
    return jsonify({"msg":f"Method must be POST"})


# add waiter using json
@app.route('/json/add', methods=['POST'])
def add_json():
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
        # message = data['message']
        # -----------------------------
        # email = request.form['email']
        # print(email)
        # message = request.form['message']
        ds = check_waiter_exists(email)
        # print(ds)
        if ds is False:
            new_waiter = Waiter(email=email)
            db.session.add(new_waiter)
            db.session.commit()
            # print("1")
            confirmation(email)
            return jsonify({"msg":f"{email} added to waitlist"})
        elif ds is True:
                # print("2")
                return jsonify({"msg":f"{email} already exists"})
    return jsonify({"msg":f"Method must be POST"})


# list out waiters, including individually
@app.route('/h/list')
def list_html():
    list = Waiter.query.order_by(Waiter.date.desc()).all()
    return render_template('list.html', list=list)

@app.route('/list')
def list():
    list = Waiter.query.order_by(Waiter.date.desc()).all()
    w_list = []
    for i in list:
        w_list.append(i.email)
    return jsonify({"count":len(w_list), "waiters":w_list,})

@app.route('/<id>/usr', methods=['GET', 'POST'])
def list_detail(id):
    waiter = Waiter.query.get(id)
    return render_template('list_detail.html', waiter=waiter)

# confirmation email
@app.route("/confirmation/<email>")
def confirmation(email):
    msg = Message('Waitlist Confirmation', recipients=[email])
    msg.html = render_template('waitlist_confirmation.html', email=email)
    mail.send(msg)
    return 'Waitlist confirmation sent to ' + email

# launch
@app.get("/launch")
def launch():
    return "Send Launch Email"

# report
@app.route("/report", methods=['GET', 'POST'])
def progress_report():
    if request.method == 'POST':
        emails = []
        waiters = Waiter.query.all()
        for i in waiters:
            emails.append(i.email)
        print(emails)
        recipients = emails
        # request.form.get('recipients').split(',')
        subject = request.form.get('subject')
        body = request.form.get('body')
        html = request.form.get('html')
        for i in emails:
            msg = Message(subject=subject, recipients=[i])
            msg.body = body
            msg.html = html
            mail.send(msg)        
        return 'Email sent!'
    return render_template('send_email.html')



# welcome

# run server
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)











