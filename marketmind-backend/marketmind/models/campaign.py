from datetime import datetime
from marketmind.extensions import db


class Campaign(db.Model):
    __tablename__ = "campaigns"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    goal = db.Column(db.String(200), nullable=True)
    target_valence = db.Column(db.Float, nullable=True)
    target_arousal = db.Column(db.Float, nullable=True)
    target_dominance = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
