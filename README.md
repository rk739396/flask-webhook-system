# Payment Webhook System (Flask)

## 📌 Overview
This project implements a minimal webhook listener system that processes payment status updates from mock providers (e.g., Razorpay/PayPal format).

It supports:
- Secure webhook verification using HMAC SHA256
- Idempotent event processing
- Storage of payment events in SQLite
- Retrieval of historical payment events

---

## ⚙️ Tech Stack
- Python 3
- Flask
- SQLite
- SQLAlchemy
- HMAC SHA256 (security simulation)

---

## 🚀 Features
- ✔ Webhook receiver endpoint
- ✔ Signature verification (HMAC-based)
- ✔ Idempotency handling (prevents duplicate events)
- ✔ Batch + single event support
- ✔ Chronological event retrieval API

---

## 📂 Project Structure
flask-webhook-system/
│
├── app.py # Main Flask application (webhook + APIs)
├── models.py # Database models (SQLAlchemy)
├── db.py # Database initialization
├── sign.py # Utility to generate HMAC signatures for testing
├── requirements.txt # Python dependencies
│
├── mock_payloads/ # Sample webhook payloads
│ ├── payment_authorized.json
│ ├── payment_captured.json
│ └── payment_failed.json
│
├── payments.db # SQLite database (auto-generated)
│
├── README.md # Project overview & setup guide
├── DOCS.md # API documentation
