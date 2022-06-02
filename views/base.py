from flask import (
Blueprint, request,  make_response, render_template, redirect, url_for, flash
)
from flask_login import login_required
from datetime import datetime, timedelta
from models import db, User, Blogpost
from rest.post import get_post, create_post

base = Blueprint('base', __name__, '')

@base.route('/')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@base.route('/about')
def about():
    return render_template('about.html')

@base.route('/post/<string:slug>')
def post(slug):
    post = get_post(slug)
    return render_template('post.html', post=post, post_header_img='home-bg.jpg')

@base.route('/add')
@login_required
def add():
    return render_template('add.html')

@base.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    slug = request.form['slug']
    author = request.form['author']
    content = request.form['content']

    create_post(title=title, subtitle=subtitle, slug=slug, author=author, \
    content=content)

    return redirect(url_for('base.index'))
