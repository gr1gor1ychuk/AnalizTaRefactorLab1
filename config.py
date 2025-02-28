# config.py

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# instantiate ap and set attributes
app1 = Flask(__name__)
app1.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app1.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app1.json.compact = False

# define metadata, set up Flask-Migrate for migrations, instantiate db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db1 = SQLAlchemy(metadata=metadata)
migrate = Migrate(app1, db1)
db1.init_app(app1)

# enables Cross-Origin Resource Sharing, allowing requests front-end
CORS(app1)

# generate a secret key in command prompt using this command:
# `python -c 'import os; print(os.urandom(16))'`
app1.config['SECRET_KEY'] = b'\x1cV\x136\xe4\xed\xdb\xb1\x04\x03*F\xdf\xe2\xd1o'
