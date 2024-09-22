from django.urls import path

from .views import (
    GenerateRecoveryCodeView,
    ResetPasswordView,
    RetrieveRecoveryCodeView,
)

urlpatterns = [
    path(
        "generate/",
        GenerateRecoveryCodeView.as_view(),
        name="recover-generate",
    ),
    path(
        "reset-password/",
        ResetPasswordView.as_view(),
        name="reset-password",
    ),
    path(
        "",
        RetrieveRecoveryCodeView.as_view(),
        name="recover",
    ),
]
