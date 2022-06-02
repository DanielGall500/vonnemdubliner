from flask import (
Blueprint, request,  make_response, render_template, redirect, url_for, flash
)
from datetime import datetime, timedelta
from flask_login import login_required
from models import db
from models import Blogpost

#GET
def get_post(slug):
    try:
        post = Blogpost.query.filter_by(slug=slug).one()
        return post
    except:
        flash("Post with slug {} not found".format(slug))
        raise

#PUT
def create_post(title, subtitle, slug, author, content):
    post = Blogpost(title=title, subtitle=subtitle, slug=slug, author=author, \
    content=content, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return post

#DELETE
def delete_post(slug):
    try:
        Blogpost.query.filterby(slug=slug).delete()
        db.session.commit()
    except:
        flash("Post with slug {} not found.".format(slug))
        raise
    return True

#POST
def update_post():
    return None
