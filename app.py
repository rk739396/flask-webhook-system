from flask import Flask, request, jsonify
from db import db
from models import PaymentEvent
import hmac
import hashlib
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///payments.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

SECRET = "test_secret"


# 🔐 Signature Verification
def verify_signature(raw_body, signature):
    expected_signature = hmac.new(
        SECRET.encode(),
        raw_body,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected_signature, signature)


# 🧾 Webhook Endpoint
@app.route("/webhook/payments", methods=["POST"])
def webhook_payments():
    signature = request.headers.get("X-Razorpay-Signature")

    if not signature:
        return jsonify({"error": "Missing signature"}), 403

    raw_body = request.data

    # 🔐 Verify signature
    if not verify_signature(raw_body, signature):
        return jsonify({"error": "Invalid signature"}), 403

    # 📦 Parse JSON
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400

    if not data:
        return jsonify({"error": "Empty payload"}), 400

    # 🧠 Support both single event and batch
    events = data if isinstance(data, list) else [data]

    processed = 0
    duplicates = 0

    try:
        for item in events:
            try:
                event_type = item["event"]
                event_id = item["id"]
                payment_id = item["payload"]["payment"]["entity"]["id"]
            except KeyError:
                return jsonify({"error": "Malformed payload"}), 400

            # 🛑 Idempotency check
            existing_event = PaymentEvent.query.filter_by(event_id=event_id).first()
            if existing_event:
                duplicates += 1
                continue

            # 💾 Store event
            event = PaymentEvent(
                event_id=event_id,
                payment_id=payment_id,
                event_type=event_type,
                payload=item
            )

            db.session.add(event)
            processed += 1

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500

    return jsonify({
        "message": "Processed",
        "processed_events": processed,
        "duplicate_events": duplicates
    }), 200


# 📊 Fetch Events
@app.route("/payments/<payment_id>/events", methods=["GET"])
def get_payment_events(payment_id):
    events = (
        PaymentEvent.query
        .filter_by(payment_id=payment_id)
        .order_by(PaymentEvent.received_at.asc())
        .all()
    )

    result = [
        {
            "event_type": e.event_type,
            "received_at": e.received_at.isoformat() + "Z"
        }
        for e in events
    ]

    return jsonify(result), 200


# 🏁 Run App
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)