from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()
password = ""
bd_name = ""

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://postgres:{password}@127.0.0.1:5432/{bd_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = ""

db.init_app(app)
migrate.init_app(app, db)

from views import *
