from flask import (
Blueprint, request,  make_response, render_template, redirect, url_for, flash
)
from flask_login import login_required
from datetime import datetime, timedelta
from vonnemdubliner.models import db, User, Blogpost
from vonnemdubliner.rest.post import get_post, create_post

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
Bring user to add post page.
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

    create_post(title=title, subtitle=subtitle, slug=slug, author=author, \
    content=content)

    return redirect(url_for('base.index'))
