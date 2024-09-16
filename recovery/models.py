from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import AllRecoveryCodeManager, RevokedRecoveryManager

# Create your models here.

User = get_user_model()


class RecoveryCode(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="recovery_codes",
    )

    code = models.CharField(
        verbose_name=_("Recovery Code"),
        max_length=16,
        editable=False,
    )
    used_at = models.DateTimeField(blank=True, null=True)
    revoked_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    objects = RevokedRecoveryManager()
    all_codes = AllRecoveryCodeManager()

    class Meta:
        verbose_name = _("Recovery Code")
        verbose_name_plural = _("Recovery Codes")

    def __str__(self) -> str:
        return f"{self.user} - {self.used}"

    @property
    def used(self) -> bool:
        return self.used_at is not None
