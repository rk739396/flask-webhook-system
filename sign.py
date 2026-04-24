import hmac, hashlib

secret = "test_secret"
body = open("mock_payloads/payment_authorized.json", "rb").read()

signature = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
print(signature)