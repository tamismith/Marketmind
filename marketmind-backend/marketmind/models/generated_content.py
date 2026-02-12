from datetime import datetime
from marketmind.extensions import db

class GeneratedContent(db.Model):
    __tablename__ = "generated_content"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    prompt = db.Column(db.Text, nullable=False)
    generated_text = db.Column(db.Text, nullable=False)

    tone = db.Column(db.String(20), nullable=False)
    sentiment_score = db.Column(db.Float, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
