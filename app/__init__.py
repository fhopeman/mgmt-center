from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, Integer, SmallInteger, Float

app = Flask(__name__)

# config db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mgmt:center@localhost/mgmtcenter'
db = SQLAlchemy(app)

# import controllers
from app import environment
from app import lights
from app import alarm
