from django.db import models
from django.conf import settings


class CalculationHistory(models.Model):
    """
    Stores calculation history for both:
    - Authenticated users (linked via user FK)
    - Guests (linked via session_key)
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='calculations'
    )

    # Used only for guest users
    session_key = models.CharField(max_length=40, null=True, blank=True)

    operand1 = models.FloatField()
    operand2 = models.FloatField()
    operator = models.CharField(max_length=1)
    result = models.FloatField()

    # Optional note (premium feature)
    note = models.TextField(max_length=500, blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        # Helpful for admin readability
        return f"{self.operand1} {self.operator} {self.operand2} = {self.result}"
