from app import app
from auth import auth
from views import views

if __name__ == '__main__':
    app.register_blueprint(auth)
    app.register_blueprint(views)
    app.run(debug=True)
