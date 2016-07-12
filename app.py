from flask import (Flask, render_template, request, make_response, redirect,
                   url_for)


app = Flask(__name__)


@app.route("/")
def home():
    username = request.cookies.get('username')
    userbirth = request.cookies.get('userbirth')
    userblood = request.cookies.get('userblood')
    return render_template("home.html", username=username,
                           userbirth=userbirth,
                           userblood=userblood)


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


@app.route('/admin/createdb')
def createdb():
    Base.metadata.create_all(engine)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run()
