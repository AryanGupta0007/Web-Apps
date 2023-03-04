from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
import datetime
auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST", "GET"])
@auth.route("/signin", methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in Successfully!", category="success")
                # users = User.query.all()
                # for user in users:
                #     print(user)
                return redirect(url_for("views.homepage", email=email))
            else:
                flash("Incorrect Password. Try again.", category="error")
        else:
            flash("User Doesn't exist. Click on Register to sign up.", category="error")        
    return render_template("login.html")

@auth.route("/logout")
@auth.route("/signout")
def signout():
    
    flash("Successfully Logged Out")
    return redirect(url_for("auth.signin"))

@auth.route("/register", methods=["POST", "GET"])
@auth.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        
        name = request.form.get('name')
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if user:
            flash("user already  exists")
            return redirect(url_for("auth.signin"))
        
        elif (password1 == password2):
            new_user = User(email=email, name=name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()            
            flash('Account created!', category='success')
            return redirect(url_for("views.homepage", email=email))
        else:
            flash("Password doesn't match")
            return render_template("signup.html")
    return render_template("signup.html")
