from django.conf import settings
from django.core.cache import cache


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