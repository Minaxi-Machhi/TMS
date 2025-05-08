import base64

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import FieldDoesNotExist
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def update_user_login_attempt(username, key_prefix, is_failed=True):
    """
    Update user login attempts in the cache.
    """
    key = f"{key_prefix}-{username}"

    if is_failed:
        attempts = cache.get(key, 0) + 1
        if attempts > 3:
            cache.set(key, attempts, timeout=settings.CACHE_TTL)
            return True
        cache.set(key, attempts, timeout=None)
    else:
        cache.delete(key)
    return False

def get_response_message(data, model, action="create"):
    return (
        f"{obj_response_message} {action}d successfully"
        if (obj_response_message := data.get('response_message', None))
        else None
    )

def get_user_full_name(self):
    try:
        if self.request.user.first_name and self.request.user.last_name:
            return f"{self.request.user.first_name} {self.request.user.last_name}"
        return self.request.user.username
    except Exception:
        return None

def is_field_in_model(model, field):
    try:
        model._meta.get_field(field)
    except FieldDoesNotExist:
        return False
    else:
        return True

def encrypt(raw):
    """ Encrypt Password"""
    raw = pad(raw.encode(), 16)
    cipher = AES.new(settings.CIPHER_KEY_PASSWORD.encode('utf-8'), AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(raw))


def decrypt(enc):
    """ Decrypt Password"""
    enc = base64.b64decode(enc)
    cipher = AES.new(settings.CIPHER_KEY_PASSWORD.encode('utf-8'), AES.MODE_ECB)
    return unpad(cipher.decrypt(enc), 16).decode()

