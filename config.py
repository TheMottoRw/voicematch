from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#sqlite_configs app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://super:super@localhost/voicematch'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
