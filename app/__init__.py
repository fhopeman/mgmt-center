from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, Integer, SmallInteger, Float

app = Flask(__name__)

# logging
import logging
from logging.handlers import TimedRotatingFileHandler

formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
handler = TimedRotatingFileHandler("logs/log", "midnight", 2)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

# config db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mgmt:center@localhost/mgmtcenter'
db = SQLAlchemy(app)

# import controllers
from app import environment
from app import lights
from app import alarm
