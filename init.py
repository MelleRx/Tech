from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:21Dima2001@127.0.0.1:5432/Kukulidi_Delivery"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = "kukulidi"

db.init_app(app)
migrate.init_app(app, db)

from views import *
