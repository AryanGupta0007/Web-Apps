from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager


DB_NAME = "database7.db"
app = Flask(__name__)
db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config["SECRET KEY"] = "DSHSHSFHAHF HSFHSKHFS"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = "jlsjfl"
    db.init_app(app=app)
    
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import  User

    with app.app_context():
        
        db.create_all()
    return app