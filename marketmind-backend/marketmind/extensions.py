from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()# database connection
migrate = Migrate() # tracks and applies database change