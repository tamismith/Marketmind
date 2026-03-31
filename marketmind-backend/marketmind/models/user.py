from datetime import datetime
from marketmind.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    credits = db.Column(db.Integer, nullable=False, default=50)
    subscription_tier = db.Column(db.String(20), nullable=False, default="free")

    generated_contents = db.relationship("GeneratedContent", backref="user", lazy=True)
    brand_memory = db.relationship("BrandMemory", backref="user", uselist=False)
    credit_transactions = db.relationship("CreditTransaction", backref="user", lazy=True)
    business_profile = db.relationship("BusinessProfile", backref="user", uselist=False)


    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
