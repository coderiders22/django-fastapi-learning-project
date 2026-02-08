from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from .models import CalculationHistory


class CalculationHistoryModelTest(TestCase):
    """Model level test"""

    def test_create_calculation_record(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )

        record = CalculationHistory.objects.create(
            user=user,
            operand1=10,
            operand2=5,
            operator="+",
            result=15
        )

        self.assertEqual(record.result, 15)
        self.assertEqual(str(record), "10.0 + 5.0 = 15.0")


class CalculatorAPITest(TestCase):
    """API tests for calculator app"""

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="apiuser",
            password="apipass"
        )

    # -------------------------------
    # GUEST CALCULATION
    # -------------------------------
    def test_guest_calculation(self):
        response = self.client.post(
            "/api/calculate/",
            {
                "operand1": 20,
                "operand2": 10,
                "operator": "-"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["result"], 10)

        self.assertEqual(CalculationHistory.objects.count(), 1)
        self.assertIsNone(CalculationHistory.objects.first().user)

    # -------------------------------
    # AUTHENTICATED CALCULATION
    # -------------------------------
    def test_authenticated_user_calculation(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            "/api/calculate/",
            {
                "operand1": 4,
                "operand2": 5,
                "operator": "*"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["result"], 20)

        record = CalculationHistory.objects.first()
        self.assertEqual(record.user, self.user)

    # -------------------------------
    # FETCH HISTORY (USER)
    # -------------------------------
    def test_fetch_user_history(self):
        self.client.force_authenticate(user=self.user)

        CalculationHistory.objects.create(
            user=self.user,
            operand1=1,
            operand2=2,
            operator="+",
            result=3
        )

        response = self.client.get("/api/history/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # -------------------------------
    # CLEAR HISTORY
    # -------------------------------
    def test_clear_history(self):
        self.client.force_authenticate(user=self.user)

        CalculationHistory.objects.create(
            user=self.user,
            operand1=5,
            operand2=5,
            operator="+",
            result=10
        )

        response = self.client.delete("/api/history/clear/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(CalculationHistory.objects.count(), 0)
