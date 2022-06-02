from flask import (
Blueprint, request,  make_response, render_template, redirect, url_for, flash
)
from datetime import datetime, timedelta
from flask_login import login_required
from vonnemdubliner.models import db
from vonnemdubliner.models import Blogpost

#GET
def get_post(slug):
    try:
        post = Blogpost.query.filter_by(slug=slug).one()
        return post
    except:
        flash("Post with slug {} not found".format(slug))
        raise

#PUT
def create_post(blogpost):
    db.session.add(blogpost)
    db.session.commit()
    return blogpost

#DELETE
def delete_post(slug):
    try:
        Blogpost.query.filterby(slug=slug).delete()
        db.session.commit()
    except:
        flash("Post with slug {} not found.".format(slug))
        raise

#POST
def update_post():
    return None
