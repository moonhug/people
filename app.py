from flask import (Flask, flash, render_template, request, session,
                   make_response, redirect, url_for)
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import random


Base = declarative_base()
engine = create_engine('sqlite:///db.db', echo=True)
Session = sessionmaker()
Session.configure(bind=engine)
db = Session()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    account = Column(String, unique=True)
    password = Column(String)
    people = relationship("People", back_populates="user")

    def __init__(self, account, password):
        self.account = account
        self.password = password

    def __repr__(self):
        return "<User('%s', '%s')>" % (self.account, self.password)


class People(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    gender = Column(String)
    sex_orientation = Column(String)
    blood = Column(String)
    strength = Column(Integer)
    mental = Column(Integer)
    intellect = Column(Integer)
    look = Column(Integer)
    charm = Column(Integer)
    will = Column(Integer)
    sincere = Column(Integer)
    morals = Column(Integer)
    faith = Column(Integer)
    stress = Column(Integer)
    tendency = Column(Integer)
    sense = Column(Integer)
    worth = Column(String)
    ideal = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="people")

    def __init__(self, name, gender, sex_orientation, blood, user_id,
    strength, mental, intellect, look, charm, will, sincere, morals, faith,
    stress, tendency, sense, worth, ideal):
        self.name = name
        self.gender = gender
        self.sex_orientation = sex_orientation
        self.blood = blood
        self.user_id = user_id
        self.strength = strength
        self.mental = mental
        self.intellect = intellect
        self.look = look
        self.charm = charm
        self.will = will
        self.sincere = sincere
        self.morals = morals
        self.faith = faith
        self.stress = stress
        self.tendency = tendency
        self.sense = sense
        self.worth = worth
        self.ideal = ideal

    def __repr__(self):
        return "<People('%s', '%s', '%s', '%s', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%s', '%s')>" \
               % (self.name, self.gender, self.sex_orientation, self.blood,
               self.strength, self.mental, self.intellect, self.look,
               self.charm, self.will, self.sincere, self.morals, self.faith,
               self.stress, self.tendency, self.sense, self.worth, self.ideal)


app = Flask(__name__)
app.config.from_pyfile('application.cfg')


def get_user(username):
    user = db.query(User).filter(User.account == username).one_or_none()
    return user


def get_current_user():
    username = session.get('username', None)
    if username:
        user = get_user(username)
        return user


@app.route("/")
def home():
    user = get_current_user()
    if user:
        people = user.people
        return render_template("people_list.html", people=people)
    else:
        return render_template("home.html")


@app.route("/set-user/", methods=['POST'])
def set_user():
    username = request.form.get('username')
    userbirth = request.form.get('userbirth')
    userblood = request.form.get('userblood')
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('username', username)
    resp.set_cookie('userbirth', userbirth)
    resp.set_cookie('userblood', userblood)
    return resp


@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/login/')
def login_form():
    return render_template("login.html")


@app.route("/login/", methods=['POST'])
def login():
    userid = request.form.get('userid')
    userpw = request.form.get('userpw')
    if userid and userpw:
        user = get_user(userid)
        if user:
            ph = PasswordHasher()
            try:
                ph.verify(user.password, userpw)
            except VerifyMismatchError:
                flash('check account or password')
            else:
                session['username'] = user.account
                flash('welcome back!')
                return redirect(url_for('home'))
        else:
            flash('check account or password')
    else:
        flash('account id or password is blank.')
    return redirect(url_for('login'))


@app.route('/join/', methods=['POST'])
def new_user():
    userid = request.form.get('userid')
    userpw = request.form.get('userpw')
    if userid and userpw:
        if db.query(User).filter(User.account == userid).first():
            flash('id already exists')
        else:
            ph = PasswordHasher()
            hash = ph.hash(userpw)
            user = User(userid, hash)
            db.add(user)
            db.commit()
            session['username'] = user.account
            flash('welcome to people!')
            return redirect(url_for('home'))
    else:
        flash('account id or password is blank.')
    return redirect(url_for('new_user'))


@app.route("/join/")
def new_user_form():
    return render_template('join.html')


@app.route("/peoplejoin/")
def new_people_form():
    return render_template('people_join.html')


@app.route('/peoplejoin/', methods=['POST'])
def new_people():
    name = request.form.get('name')
    gender = request.form.get('gender')
    sex_orientation = request.form.get('sex_orientation')
    bloodtype = request.form.get('bloodtype')
    strength = random.randrange(5, 11)
    mental = random.randrange(5, 11)
    intellect = random.randrange(5, 11)
    look = random.randrange(5, 11)
    charm = random.randrange(5, 11)
    will = random.randrange(5, 11)
    sincere = random.randrange(5, 11)
    morals = random.randrange(5, 11)
    faith = random.randrange(5, 11)
    stress = 0
    tendency = request.form.get('tendency')
    sense = request.form.get('sense')
    worth = request.form.get('worth')
    ideal = request.form.get('ideal')
    if name:
        if db.query(People).filter(People.name == name).first():
            flash('name already exists')
        else:
            people = People(name, gender, sex_orientation, bloodtype,
                            get_current_user().id,
                            strength, mental, intellect, look, charm,
                            will, sincere, morals, faith, stress,
                            tendency, sense, worth, ideal)
            db.add(people)
            db.commit()
            flash('welcome to people!')
            return redirect(url_for('home'))
    else:
        flash('check the input form')
    return redirect(url_for('new_people'))


@app.route('/admin/users/')
def user_list():
    users = db.query(User).all()
    return render_template('user_list.html', users=users)


@app.route('/admin/createdb')
def createdb():
    Base.metadata.create_all(engine)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run()
