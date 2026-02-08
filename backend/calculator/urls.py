from django.urls import path
from .auth_views import (
    RegisterView,
    LoginView,
    LogoutView,
    MeView,
    CSRFView
)
from .views import (
    CalculateView,
    HistoryView,
    clear_history,
    delete_history_item
)

urlpatterns = [
    # AUTH
    path("auth/csrf/", CSRFView.as_view()),
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", LoginView.as_view()),
    path("auth/logout/", LogoutView.as_view()),
    path("auth/me/", MeView.as_view()),

    # CALCULATOR
    path("calculate/", CalculateView.as_view()),
    path("history/", HistoryView.as_view()),
    path("history/clear/", clear_history),
    path("history/<int:pk>/", delete_history_item),
]
