from django.contrib import admin
from .models import CalculationHistory


@admin.register(CalculationHistory)
class CalculationHistoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for CalculationHistory model.

    Purpose:
    - Allow admin to VIEW calculation records
    - Prevent manual tampering (no add/edit/delete)
    - Useful for monitoring user & guest activity
    """

    # Fields visible in admin list view
    list_display = (
        "id",
        "user",
        "session_key",
        "operand1",
        "operator",
        "operand2",
        "result",
        "created_at",
    )

    # Filters to quickly narrow results
    list_filter = ("operator", "created_at")

    # Search by username (logged-in users) or session key (guests)
    search_fields = ("user__username", "session_key")

    # Default ordering (latest first)
    ordering = ("-created_at",)

    # Make all fields read-only to avoid data manipulation
    readonly_fields = (
        "user",
        "session_key",
        "operand1",
        "operator",
        "operand2",
        "result",
        "created_at",
    )

    # Prevent adding records manually from admin
    def has_add_permission(self, request):
        return False

    # Prevent deleting records
    def has_delete_permission(self, request, obj=None):
        return False

    # Prevent editing records
    def has_change_permission(self, request, obj=None):
        return False
