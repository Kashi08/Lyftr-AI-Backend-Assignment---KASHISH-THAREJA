import hmac
import hashlib
import os

def verify_signature(payload: bytes, signature: str):
    secret = os.getenv("WEBHOOK_SECRET")
    if not secret:
        return False
   
    expected_signature = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature)