from datetime import datetime
from marketmind.extensions import db


class CreditTransaction(db.Model):
    __tablename__ = "credit_transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Positive = credits added, negative = credits deducted
    amount = db.Column(db.Integer, nullable=False)

    # "purchase" | "deduction"
    transaction_type = db.Column(db.String(20), nullable=False)

    # Human-readable description e.g. "Text A/B generation" or "Starter plan purchase"
    description = db.Column(db.String(200), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
