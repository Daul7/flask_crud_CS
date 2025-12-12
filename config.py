# app.py
from flask import Flask, request, jsonify, make_response
from flask_mysqldb import MySQL
from dicttoxml import dicttoxml
import jwt, datetime
from functools import wraps
from flask_bcrypt import Bcrypt
import config  # import your config file

app = Flask(__name__)

# Load config
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB
app.config['MYSQL_CURSORCLASS'] = config.MYSQL_CURSORCLASS
app.config['SECRET_KEY'] = config.SECRET_KEY
