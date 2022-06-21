from flask import (
Blueprint, request,  make_response, render_template, redirect, url_for, flash
)
from flask_login import login_required
from datetime import datetime, timedelta
from vonnemdubliner.models import db, User, Blogpost
from vonnemdubliner.rest.post import get_post, create_post, update_post
from werkzeug.utils import secure_filename
from app import UPLOAD_FOLDER
import pathlib
import os

base = Blueprint('base', __name__, '')

"""
HOME
The home page of the vnD project.
"""
@base.route('/')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

"""
HOME
Simple page to display an intro to the vnD project.
"""
@base.route('/about')
def about():
    return render_template('about.html')

"""
POST
Display a post when given a slug.
"""
@base.route('/post/<string:slug>')
def post(slug):
    post = get_post(slug)
    return render_template('post.html', post=post, post_header_img='home-bg.jpg')

"""
ADD POST
Bring user to add post page to fill out new post form.
Can add main content and images.
Must be logged in as admin user.
"""
@base.route('/add', methods=['POST','GET'])
@login_required
def add():
    #If no post has been submitted, load the -add post- form
    if request.method == 'GET':
        return render_template('add.html')

    #If a post has been submitted, add to the database and redirect
    title = request.form['title']
    subtitle = request.form['subtitle']
    slug = request.form['slug']
    author = request.form['author']
    content = request.form['content']
    curr_time = datetime.now()

    new_post = Blogpost(title=title, subtitle=subtitle, slug=slug, author=author, \
    content=content, date_posted=curr_time)
    create_post(new_post)

    if "images" in request.files:
        uploaded_files = request.files.getlist('images')
        post_id = str(get_post(slug).id)
        print(post_id)
        pathlib.Path(UPLOAD_FOLDER, post_id).mkdir(exist_ok=True)
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, post_id, filename))

    return redirect(url_for('base.index'))

"""
EDIT POST
Edit a post.
"""
@base.route('/edit/<string:slug>', methods=['POST','GET'])
@login_required
def edit(slug):
    post = get_post(slug)
    id = post.id

    if request.method == 'GET':
        return render_template('edit.html', post=post)

    #Store the updated post information
    edit_form = request.form
    post.title = edit_form['title']
    post.subtitle = edit_form['subtitle']
    post.slug = edit_form['slug']
    post.content = edit_form['content']

    update_post(id, post)
    return redirect(url_for('base.post',slug=post.slug))
