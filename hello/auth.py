import hmac
import json
import logging
import os

logger = logging.getLogger(__name__)

def get_key_bytes():
    key = os.environ['SECRET_TOKEN']
    return key.encode()

def compute_github_hmac_json(json_payload: str):
    # https://developer.github.com/webhooks/securing/#setting-your-secret-token
    # https://developer.github.com/webhooks/#delivery-headers
    # https://gist.github.com/categulario/deeb41c402c800d1f6e6#gistcomment-2927474
    content = json.dumps(json.loads(json_payload), separators=(',',':')).encode()
    return hmac.new(get_key_bytes(), content, "sha1").hexdigest()

def compute_github_hmac(bytes_value):
    return hmac.new(get_key_bytes(), bytes_value, "sha1").hexdigest()

def authenticate_github_webhook_request(request):
    sender_hmac_header = request.headers['X-Hub-Signature']
    sender_hmac = sender_hmac_header.split("=")[1]
    logger.warning(f"authenticate_github_webhook_request: {request.body}.")
    computed_hmac = compute_github_hmac(request.body)
    logger.warning(f"authenticate_github_webhook_request: {sender_hmac} : {computed_hmac}.")
    if sender_hmac != computed_hmac:
        raise Exception("HMAC does not match.")
