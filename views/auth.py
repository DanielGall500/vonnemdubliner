from flask import (
Blueprint, request, jsonify, make_response, render_template, redirect, url_for, flash
)
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from models import db, User, Blogpost
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'GET':
        return render_template('login.html')

    #Otherwise, handle login POST data
    auth = request.form
    if not auth or not auth.get('username') or not auth.get('password'):
        return make_response('Could not verify!', 401, \
        {'WWW-Authenticate':'Basic-realm= "Login Required!"'})

    _username = auth.get('username')
    _password = auth.get('password')
    user = User.query.filter_by(username=_username).first()
    if not user:
        return make_response('Could not verify user, please sign up.', 401, \
        {'WWW-Authenticate':'Basic-realm= "No user found!"'})

    if check_password_hash(user.password, _password):
        #token = jwt.encode({'public_id':user.public_id}, \
        #app.config['SECRET_KEY'], 'HS256')
        #return make_response(jsonify({'x-access-token':token}),201)
        flash("Logged In!",category='success')
        login_user(user,remember=True)
        return redirect(url_for('views.add'))

    return make_response("Could not verify password!",403,\
    {'WWW-Authenticate': 'Basic-realm= "Wrong Password!"'})

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged Out.")
    return redirect(url_for('views.index'))
