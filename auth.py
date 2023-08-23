from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route("/masuk")
def login():
    return render_template("login.html")

@auth.route('/masuk', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Email atau Password salah')
        return redirect(url_for('auth.login'))

    login_user(user)

    return redirect(url_for('homepage.index'))

@auth.route('/daftar')
def daftar():
    return render_template('register.html')

@auth.route('/daftar', methods=['POST'])
def daftar_post():
    name = request.form.get('name')
    nomorhp = request.form.get('nomorhp')
    email = request.form.get('email')
    password = request.form.get('password')
    repassword = request.form.get('repassword')

    user = User.query.filter_by(email=email).first()

    admin = User.query.filter_by(lvl='1').first()
    if not admin:
        lvl = "1"
    else:
        lvl = "5"

    if user: 
        flash('Email telah digunakan')
        return redirect(url_for('auth.daftar'))

    if password != repassword:
        flash(u'Password berbeda', 'pass-error')
        return redirect(url_for('auth.daftar'))

    new_user = User(email=email, nama=name, nomorhp = nomorhp, password=generate_password_hash(password, method='sha256'), lvl=lvl)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage.home'))
