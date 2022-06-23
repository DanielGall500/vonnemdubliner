from wtforms import (
StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
)
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField
from flask_wtf import FlaskForm

class BlogpostForm(FlaskForm):
    title = StringField('title',
        [
            DataRequired(message="Enter a title.")
        ]
    )
    subtitle = StringField('subtitle',
        []
    )
    slug = StringField("slug",
        [
            DataRequired(message="Enter a slug.")
        ]
    )
    author = StringField('author',
        [
            DataRequired(message="Enter the author name.")
        ]
    )
    images = FileField('images',
        []
    )
    content = CKEditorField('content',
        [
            DataRequired()
        ]
    )

    submit = SubmitField('submit')
