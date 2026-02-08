from rest_framework import serializers
from .models import CalculationHistory


class CalculationHistorySerializer(serializers.ModelSerializer):
    """
    Controls how calculation history is sent to frontend.
    """

    class Meta:
        model = CalculationHistory
        fields = [
            "id",
            "operand1",
            "operand2",
            "operator",
            "result",
            "note",
            "created_at",
        ]

        # These fields should never be modified from frontend
        read_only_fields = ['id', 'created_at']
