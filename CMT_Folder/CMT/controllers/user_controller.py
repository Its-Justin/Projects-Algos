from flask import render_template, session, redirect, request, flash
from CMT.models import user
from CMT import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def reroute():
    return redirect("/register-login")

@app.route('/register-login')
def register_login():
    return render_template("register_login.html")

@app.route('/register', methods=['POST'])
def insert_user():
    if not user.User.validate_user_register(request.form):
        return redirect("/register-login")
    else:
        hashed_password = bcrypt.generate_password_hash(request.form["password"])
        new_user =  {
            "name": request.form["name"],
            "username": request.form["username"],
            "password": hashed_password
        }
        new_user_id = user.User.create_user(new_user)
        session["id"] = new_user_id
        session["username"] = request.form["username"]
        return redirect("/home")

@app.route('/login', methods=['POST'])
def verify_user():
    if not user.User.validate_user_login(request.form):
        return redirect("/register-login")
    else:
        user_in_db = user.User.get_user_by_username({"username": request.form["username"]})
        session.clear()
        session["id"] = user_in_db.id
        session["username"] = user_in_db.username
        return redirect("/home")

@app.route('/logout')
def sign_out():
    session.clear()
    return redirect("/register-login")