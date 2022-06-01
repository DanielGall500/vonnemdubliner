from flask import (
Blueprint, request,  make_response, render_template, redirect, url_for, flash
)
from flask_login import login_required
from datetime import datetime, timedelta
from app import app, db
from models import User, Blogpost

base = Blueprint('base', __name__, '')

@base.route('/')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@base.route('/about')
def about():
    return render_template('about.html')

@base.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    return render_template('post.html', post=post, post_header_img='home-bg.jpg')

@base.route('/add')
@login_required
def add():
    return render_template('add.html')

@base.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('views.index'))
