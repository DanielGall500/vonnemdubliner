from app import app
from views.auth import auth
from views.base import base

if __name__ == '__main__':
    app.register_blueprint(auth)
    app.register_blueprint(base)
    app.run(debug=True)
