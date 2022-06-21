from flask import (
Blueprint, request,  make_response, render_template, redirect, url_for, flash
)
from datetime import datetime, timedelta
from flask_login import login_required
from vonnemdubliner.models import db
from vonnemdubliner.models import Blogpost
from app import UPLOAD_FOLDER
import shutil
import pathlib

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
        #Load post data
        id = str(get_post(slug).id)

        #Delete post from SQL database
        Blogpost.query.filter_by(id=id).delete()
        db.session.commit()

        #Delete all files associated with the post
        images_path = pathlib.Path(UPLOAD_FOLDER, id)
        shutil.rmtree(images_path)
    except:
        flash("Post with slug {} not found.".format(slug))
        raise

"""
UPDATE
Filters by the slug and updates the content of the post
if one is available.
"""
def update_post(id, post):
    try:
        db.session.add(post)
        db.session.commit()
    except:
        raise
