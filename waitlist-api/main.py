from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'UHURIY7I7IY2C4T.feyafinnryeniyw/rww'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///waitlinkr.db'
db = SQLAlchemy(app)

app.app_context().push()

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
    return jsonify({"waiters":w_list})

@app.route('/<id>/usr', methods=['GET', 'POST'])
def list_detail(id):
    waiter = Waiter.query.get(id)
    return render_template('list_detail.html', waiter=waiter)

# launch

# report

# welcome

# run server
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
