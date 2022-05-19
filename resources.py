from flask import request, jsonify, make_response, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid
from datetime import datetime, timedelta
from app import app, db
from models import User, Blogpost, token_required

@app.route('/')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    return render_template('post.html', post=post, post_header_img='home-bg.jpg')

@app.route('/add')
@token_required
def add():
    return render_template('add.html')

@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/admin', methods=['POST'])
def admin():
    auth = request.get_json()
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
        token = jwt.encode({'public_id':user.public_id}, \
        app.config['SECRET_KEY'], 'HS256')
        return make_response(jsonify({'token':token}),201)

    return make_response("Could not verify password!",403,\
    {'WWW-Authenticate': 'Basic-realm= "Wrong Password!"'})
