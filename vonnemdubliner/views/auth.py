from flask import (
Blueprint, request, jsonify, make_response, render_template, redirect, url_for, flash
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from vonnemdubliner.models import db, User, Blogpost
from werkzeug.utils import secure_filename
from app import UPLOAD_FOLDER
import pathlib
import uuid
import os

auth = Blueprint('auth', __name__, url_prefix='/auth')

"""
ADMIN
Handles the logging in of admin users that are allowed
to create and edit posts.
"""
@auth.route('/admin', methods=['POST', 'GET'])
def admin():
    #If a form has not been submitted, load the login form
    if request.method == 'GET':
        return render_template('login.html')

    #If a form has been submitted, load the form data
    auth = request.form
    if not auth or not auth.get('username') or not auth.get('password'):
        return make_response('Could not verify!', 401, \
        {'WWW-Authenticate':'Basic-realm= "Login Required!"'})

    #Handle username and password
    _username = auth.get('username')
    _password = auth.get('password')
    user = User.query.filter_by(username=_username).first()
    if not user:
        return make_response('Could not verify user, please sign up.', 401, \
        {'WWW-Authenticate':'Basic-realm= "No user found!"'})

    #As soon as the password is verified, load the -add post- page.
    if check_password_hash(user.password, _password):
        flash("Logged In!",category='success')
        login_user(user,remember=True)
        return redirect(url_for('base.index'))

    return make_response("Could not verify password!",403,\
    {'WWW-Authenticate': 'Basic-realm= "Wrong Password!"'})

"""
LOG OUT
Logs the current user out and returns to home page.
"""
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged Out.")
    return redirect(url_for('base.index'))

"""
UPLOAD IMAGES
Allows an admin to upload images for use in a post.
"""
@auth.route("/uploads", methods=["GET","POST"])
@login_required
def uploads():
    if request.method == "POST" and "photos" in request.files:
        uploaded_files = request.files.getlist('photos')
        post_id = request.form['post_id']
        filename = []
        pathlib.Path(UPLOAD_FOLDER, post_id).mkdir(exist_ok=True)
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER,post_id,filename))
        return post_id
    return redirect(url_for('base.index'))
