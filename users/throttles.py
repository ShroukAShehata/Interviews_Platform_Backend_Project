# users/throttles.py

from rest_framework.throttling import SimpleRateThrottle
from django.conf import settings


class LoginRateThrottle(SimpleRateThrottle):
    """
    Throttle login attempts per IP address.
    Uses scope 'login' mapped to DEFAULT_THROTTLE_RATES['login'].
    """
    scope = "login"

    def get_cache_key(self, request, view):
        # get_ident is provided by SimpleRateThrottle uses request.META["REMOTE_ADDR"] internally to get client IP
        ident = self.get_ident(request)
        if not ident:
            return None
        #generate key in this format: throttle_{scope}_{IP}
        return self.cache_format % {"scope": self.scope, "ident": ident}


class RoleBasedUserThrottle(SimpleRateThrottle):
    """
    Throttle per authenticated user, rate depends on user.role.
    Uses scope names equal to role names defined in DEFAULT_THROTTLE_RATES["expert"/ "explorer"/ "admin"].
    """

    scope = None

    def get_cache_key(self, request, view):
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            # Use IP fallback for anonymous users
            ident = self.get_ident(request)
            return self.cache_format % {"scope": "anon", "ident": ident}
        
        role = getattr(user, "role", None) or "explorer"
        ident = f"user-{user.id}"
        return self.cache_format % {"scope": role, "ident": ident}


class ScopedPerIPThrottle(SimpleRateThrottle):
    """
    Example: Scoped throttle that keys by IP + scope.
    """
    # scope will be set on the view (throttle_scope = "analytics" etc.)
    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        if not ident:
            return None
        return self.cache_format % {"scope": self.scope, "ident": ident}
