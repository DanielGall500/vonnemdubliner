from vonnemdubliner.rest.post import create_post
from vonnemdubliner.models import db, Blogpost

def test_new_post(new_post):
    """
    GIVEN a Blogpost model
    WHEN a new Blogpost is created
    THEN check title, subtitle, slug, author,
    and content fields are defined correctly
    """
    assert new_post.title == 'test-title'
    assert new_post.subtitle == 'test-subtitle'
    assert new_post.slug == 'test-slug'
    assert new_post.author == 'test-author'
    assert new_post.content == 'test-content'

def test_new_post_in_database(app, new_post):
    with app.app_context():
        create_post(new_post)
        assert Blogpost.query.filterby(slug=new_post.slug).count() == 1
