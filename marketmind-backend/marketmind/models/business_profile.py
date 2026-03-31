from datetime import datetime
from marketmind.extensions import db


class BusinessProfile(db.Model):
    __tablename__ = "business_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)

    business_name = db.Column(db.String(120), nullable=True)
    industry = db.Column(db.String(120), nullable=True)
    target_audience = db.Column(db.String(200), nullable=True)
    region = db.Column(db.String(80), nullable=True)
    website = db.Column(db.String(200), nullable=True)
    logo_base64 = db.Column(db.Text, nullable=True)

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
