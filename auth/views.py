import ldap
from flask import request, render_template, flash, redirect, \
    url_for, Blueprint, g, Response
from flask_login import current_user, login_user, \
    logout_user, login_required
from pyxis import login_manager, db
from pyxis.auth.models import User, LoginForm
 
auth = Blueprint('auth', __name__)
 
 
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
 
 
@auth.before_request
def get_current_user():
    g.user = current_user
 
 
@auth.route('/')
@auth.route('/home')
@login_required
def home():
    # return render_template('home.html')
    return Response('Login OK', 200, {})


@auth.route('/check')
def check():
    print('___---> USER')
    print(current_user)
    print(request)
    print(request.form)
    if current_user.is_authenticated:
        flash('You are already logged in.')
        # return redirect(url_for('auth.home'))
        return Response('Login OK', 200, {})

    return Response('No authenticated', 401, {})

 
@auth.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        flash('You are already logged in.')
        # return redirect(url_for('auth.home'))
        return Response('Login OK', 200, {})
    
    form = LoginForm(request.form)
 
    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')
 
        try:
            User.try_login(username, password)
        except ldap.INVALID_CREDENTIALS:
            flash(
                'Invalid username or password. Please try again.',
                'danger')
            return render_template('login.html', form=form)
            # return Response('Invalid username or password', 401, {})
 
        user = User.query.filter_by(username=username).first()
 
        if not user:
            print('NAO TEM USER!!!!!!')
            user = User(username, password)
            db.session.add(user)
            db.session.commit()
        else:
            print('JA TEM USER')
        login_user(user)
        flash('You have successfully logged in.', 'success')
        return Response('Login OK', 200, {})
 
    if form.errors:
        flash(form.errors, 'danger')
 
    return render_template('login.html', form=form)
 
 
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))