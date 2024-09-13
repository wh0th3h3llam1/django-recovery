from django.db.models.manager import Manager
from django.db.models.query import QuerySet


class RevokedRecoveryManager(Manager):

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().exclude(revoked_at__isnull=False)


class AllRecoveryCodeManager(Manager):

    pass
