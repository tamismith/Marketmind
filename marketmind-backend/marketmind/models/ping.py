from datetime import datetime
from marketmind.extensions import db

class Ping(db.Model):

    __tablename__ = "ping"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(50), nullable=False, default="ok")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
