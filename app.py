from flask import Flask
from flask_cors import CORS
from models import db
from routes import routes_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)

app.register_blueprint(routes_bp)

if __name__ == '__main__':
    app.run(debug=True)
