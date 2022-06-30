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
def get_posts(slug=None,id=None):
    if slug:
        return Blogpost.query.filter_by(slug=slug)
    elif id:
        return Blogpost.query.filter_by(id=id)
    return None

def get_post(slug=None, id=None):
    return get_posts(slug=slug,id=id).one()

"""
CREATE
Adds & commits the HTML of a post to the database.
"""
def add_post(blogpost):
    db.session.add(blogpost)
    db.session.commit()
    return blogpost

"""
DELETE
Filters by the slug and deletes a post with that slug if available.
"""
def delete_post(slug):
    post = get_post(slug=slug)
    if not post:
        return False

    id = str(post.id)
    get_posts(id=id).delete()
    delete_images(id)

    db.session.commit()
    return True

def delete_images(id):
    images_path = pathlib.Path(UPLOAD_FOLDER, id)
    if images_path.is_dir():
        shutil.rmtree(images_path)

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
        return False
    return True
