from flask import Flask, render_template, flash, redirect, request
from urllib.parse import urlsplit
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
import sqlalchemy as sa
import logging



@app.route('/')
@app.route('/index')
@login_required
def index():
    app.logger.info('Index page hit.')
    return render_template('index.html', title='ACS Invent Home Page')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        app.logger.info('User already authenticated.')
        return redirect('/index')
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            app.logger.info('Invalid username or password.')
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = '/index'
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    app.logger.info('User logged out.')
    return redirect('/index')

@app.route('/register', methods=['GET', 'POST'])
def register():
    app.logger.info('Register page hit.')
    if current_user.is_authenticated:
        app.logger.info('User already authenticated.')
        return redirect('/index')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        app.logger.info('User registered.')
        flash('Congratulations, you are now a registered user!')
        return redirect('/login')
    return render_template('register.html', title='Register', form=form)
