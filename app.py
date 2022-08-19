import os
from flask import Flask, got_request_exception, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:amin@123@localhost:3306/sharebite'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from views import *
from models import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, use_reloader=True, threaded=True)