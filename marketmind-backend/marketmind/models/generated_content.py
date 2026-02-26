from datetime import datetime
from marketmind.extensions import db

class GeneratedContent(db.Model):
    __tablename__ = "generated_content"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    original_prompt = db.Column(db.Text, nullable=False)
    variant_a_text = db.Column(db.Text, nullable=False)
    variant_b_text = db.Column(db.Text, nullable=False)
    variant_a_eval_json = db.Column(db.JSON, nullable=False)
    variant_b_eval_json = db.Column(db.JSON, nullable=False)
    selected_variant = db.Column(db.String(1), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
