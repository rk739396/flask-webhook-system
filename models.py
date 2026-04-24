from db import db
from datetime import datetime

class PaymentEvent(db.Model):
    __tablename__ = "payment_events"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String, unique=True, nullable=False)
    payment_id = db.Column(db.String, nullable=False)
    event_type = db.Column(db.String, nullable=False)
    payload = db.Column(db.JSON, nullable=False)
    received_at = db.Column(db.DateTime, default=datetime.utcnow)