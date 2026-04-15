from datetime import datetime

from marketmind.extensions import db


class BrandMemory(db.Model):
    __tablename__ = "brand_memory"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)

    preferred_tone = db.Column(db.String(80), nullable=True)
    preferred_creativity = db.Column(db.Float, nullable=True, default=0.5)
    preferred_platform = db.Column(db.String(80), nullable=True)
    preferred_region = db.Column(db.String(80), nullable=True)
    style_notes = db.Column(db.Text, nullable=True)
    cta_preferences = db.Column(db.Text, nullable=True)

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
