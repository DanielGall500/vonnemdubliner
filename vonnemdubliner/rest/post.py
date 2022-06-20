from flask import (
Blueprint, request,  make_response, render_template, redirect, url_for, flash
)
from datetime import datetime, timedelta
from flask_login import login_required
from vonnemdubliner.models import db
from vonnemdubliner.models import Blogpost

"""
GET
Filters by the slug and returns a post if available.
"""
def get_post(slug):
    try:
        post = Blogpost.query.filter_by(slug=slug).one()
        return post
    except:
        flash("Post with slug {} not found".format(slug))
        raise

"""
CREATE
Adds & commits the HTML of a post to the database.
"""
def create_post(blogpost):
    db.session.add(blogpost)
    db.session.commit()
    return blogpost

"""
DELETE
Filters by the slug and deletes a post with that slug if available.
"""
def delete_post(slug):
    try:
        Blogpost.query.filterby(slug=slug).delete()
        db.session.commit()
    except:
        flash("Post with slug {} not found.".format(slug))
        raise

"""
UPDATE
Filters by the slug and updates the content of the post
if one is available.
"""
def update_post(slug, content):
    try:
        Blogpost.query.filterby(slug=slug).\
        update({'content': content})
        db.session.commit()
    except:
        flash("Post with slug {} not found.".format(slug))
        raise
