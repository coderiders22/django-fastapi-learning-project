from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .models import CalculationHistory
from .serializers import CalculationHistorySerializer
from .authentication import CsrfExemptSessionAuthentication


# =========================
# CALCULATE
# =========================
class CalculateView(APIView):
    """
    Handles calculator logic.

    Rules:
    - Authenticated users:
        - Unlimited calculations
        - Unlimited notes
    - Guest users:
        - Max 10 calculations
        - Notes allowed only in 2 calculations
    """

    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        # -------------------------
        # Input validation
        # -------------------------
        try:
            a = float(request.data.get("operand1"))
            b = float(request.data.get("operand2"))
            op = request.data.get("operator")
            note = request.data.get("note", "").strip()
        except Exception:
            return Response({"error": "Invalid input"}, status=400)

        if op not in ["+", "-", "*", "/"]:
            return Response({"error": "Invalid operator"}, status=400)

        if op == "/" and b == 0:
            return Response({"error": "Division by zero"}, status=400)

        # -------------------------
        # Safe calculation
        # -------------------------
        result = eval(f"{a}{op}{b}")

        data = {
            "operand1": a,
            "operand2": b,
            "operator": op,
            "result": result,
            "note": note[:500],  # hard limit for safety
        }

        # =========================
        # AUTHENTICATED USER
        # =========================
        if request.user.is_authenticated:
            data["user"] = request.user

        # =========================
        # GUEST USER
        # =========================
        else:
            # Ensure session exists
            if not request.session.session_key:
                request.session.create()

            session_key = request.session.session_key
            data["session_key"] = session_key

            # ---- Guest calculation limit (10) ----
            total_guest_calculations = CalculationHistory.objects.filter(
                session_key=session_key
            ).count()

            if total_guest_calculations >= 10:
                return Response(
                    {
                        "error": "Guest calculation limit reached. Login to unlock full access."
                    },
                    status=403
                )

            # ---- Guest note limit (ONLY 2 notes allowed) ----
            if note:
                guest_notes_count = CalculationHistory.objects.filter(
                    session_key=session_key
                ).exclude(note="").count()

                if guest_notes_count >= 2:
                    return Response(
                        {
                            "error": (
                                "Guest note limit reached. "
                                "You can add notes to only 2 calculations. "
                                "Login for unlimited notes."
                            )
                        },
                        status=403
                    )

        # -------------------------
        # Save calculation
        # -------------------------
        CalculationHistory.objects.create(**data)

        return Response(
            {"saved": True, "result": result},
            status=201
        )


# =========================
# HISTORY
# =========================
class HistoryView(APIView):
    """
    Returns calculation history:
    - Logged-in user → full history
    - Guest → last 10 calculations (session-based)
    """

    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            history = CalculationHistory.objects.filter(user=request.user)
        else:
            if not request.session.session_key:
                return Response([])
            history = CalculationHistory.objects.filter(
                session_key=request.session.session_key
            )

        serializer = CalculationHistorySerializer(
            history.order_by("-created_at"),
            many=True
        )
        return Response(serializer.data)


# =========================
# CLEAR HISTORY
# =========================
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
@authentication_classes([CsrfExemptSessionAuthentication])
def clear_history(request):
    """
    Clears all calculation history for logged-in user.
    Guests are not allowed to clear history.
    """
    CalculationHistory.objects.filter(user=request.user).delete()
    return Response({"detail": "History cleared"})


# =========================
# DELETE SINGLE ITEM
# =========================
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
@authentication_classes([CsrfExemptSessionAuthentication])
def delete_history_item(request, pk):
    """
    Deletes a single calculation record for logged-in user.
    """
    CalculationHistory.objects.filter(
        id=pk,
        user=request.user
    ).delete()

    return Response({"detail": "Deleted"})
