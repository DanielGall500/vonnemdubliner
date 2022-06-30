from flask import (
    Blueprint, request,  make_response, render_template, redirect, url_for, flash
)
from werkzeug.utils import secure_filename
from app import UPLOAD_FOLDER
import pathlib
import os

"""
ADD
Add an image to our media folder for a specific post.
"""
def add_image(file):
    pathlib.Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return url_for('auth.uploaded_files', filename=file.filename)
