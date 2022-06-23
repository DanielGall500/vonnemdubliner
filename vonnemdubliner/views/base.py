from flask import (
    Blueprint, request,  make_response, render_template, redirect, url_for, flash
)
from vonnemdubliner.rest.post import (
    get_post, create_post, delete_post, update_post
)
from vonnemdubliner.models import db, User, Blogpost
from vonnemdubliner.webforms import BlogpostForm
from flask_login import login_required
from datetime import datetime, timedelta
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
    post = get_post(slug=slug)
    return render_template(
        'post.html',
        post=post,
        post_header_img='home-bg.jpg'
    )

"""
ADD POST
Bring user to add post page to fill out new post form.
Can add main content and images.
Must be logged in as admin user.
"""
@base.route('/add', methods=['POST','GET'])
@login_required
def add():
    blogpost_form = BlogpostForm()

    if is_form_submitted(request):
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

        #Make REST
        if "images" in request.files:
            uploaded_files = request.files.getlist('images')
            post_id = str(get_post(slug).id)
            pathlib.Path(UPLOAD_FOLDER, post_id).mkdir(exist_ok=True)
            for file in uploaded_files:
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, post_id, filename))

        return redirect(
            url_for('base.index')
        )
    else:
        return render_template(
            'add.html',
            form=blogpost_form
        )


"""
EDIT POST
Edit a post.
"""
@base.route('/edit/<string:slug>', methods=['POST','GET'])
@login_required
def edit(slug):
    edit_form = BlogpostForm()
    print(slug)
    post = get_post(slug)
    id = post.id

    if is_form_submitted(request):
        edit_form = request.form
        post.title = edit_form['title']
        post.subtitle = edit_form['subtitle']
        post.slug = edit_form['slug']
        post.content = edit_form['content']
        update_post(id, post)

        return redirect(
            url_for(
                'base.post',
                slug=post.slug
            )
        )
    else:
        edit_form.title.data = post.title
        edit_form.subtitle.data = post.subtitle
        edit_form.slug.data = post.slug
        edit_form.content.data = post.content

        return render_template(
            'edit.html',
            form=edit_form,
            post=post
        )

"""
DELETE POST
Delete a post from the SQL database.
"""
@base.route('/delete/<string:slug>', methods=["POST","GET"])
@login_required
def delete(slug):
    post = get_post(slug)

    if is_form_submitted(request):
        delete_form = request.form
        delete_post_confirmed = (delete_form['radio-toggle'] == "toggle-yes")

        if delete_post_confirmed:
            delete_post(slug)

        return redirect(
            url_for('base.index')
        )
    else:
        return render_template(
            'delete.html',
            post=post
        )

"""
HELPER FUNCTIONS
Functions that help improve code readability and coherence.
"""
def is_form_submitted(request):
    return request.method == "POST"
