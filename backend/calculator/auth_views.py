from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .authentication import CsrfExemptSessionAuthentication


# =========================
# CSRF COOKIE ENDPOINT
# =========================
@method_decorator(ensure_csrf_cookie, name="dispatch")
class CSRFView(APIView):
    """
    Called once from frontend on app load.
    Purpose:
    - Sets CSRF cookie in browser
    - Required for session-based authentication
    """
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"detail": "CSRF cookie set"})


# =========================
# REGISTER
# =========================


class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required"},
                status=400
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"username": ["This username is already taken. Please choose another one."]},
                status=400
            )

        # 🔐 Strong password validation
        try:
            validate_password(password, user=User(username=username))
        except ValidationError as e:
            return Response(
                {
                    "password": e.messages
                },
                status=400
            )

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)
        request.session.save()

        return Response(
            {
                "message": "Account created successfully",
                "username": user.username
            },
            status=201
        )


# =========================
# LOGIN
# =========================
class LoginView(APIView):
    """
    Logs user in using Django session authentication.
    """

    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=401)

        login(request, user)
        request.session.save()

        return Response({
            "message": "Login successful",
            "username": user.username,
            "is_authenticated": True
        })


# =========================
# LOGOUT
# =========================
class LogoutView(APIView):
    """
    Logs out authenticated user.
    Session is fully cleared.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        logout(request)
        request.session.flush()
        return Response({"message": "Logged out successfully"})


# =========================
# AUTH STATUS
# =========================
class MeView(APIView):
    """
    Used by frontend to check:
    - Is user logged in?
    - What is the username?
    """

    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                "is_authenticated": True,
                "username": request.user.username
            })
        return Response({"is_authenticated": False})
