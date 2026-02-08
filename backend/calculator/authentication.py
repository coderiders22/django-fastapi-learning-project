from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Custom session authentication.

    Why this exists:
    - Frontend (Vue + Axios) already handles CSRF via cookies
    - DRF by default blocks POST/DELETE without CSRF token
    - This class disables DRF's strict CSRF enforcement
    - Django's CSRF middleware still protects normal views
    """

    def enforce_csrf(self, request):
        # Overriding default behavior to skip CSRF validation
        return
