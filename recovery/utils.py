import secrets
from django.contrib.auth import get_user_model

from .models import RecoveryCode

User = get_user_model()


def get_recovery_code() -> int:
    return secrets.choice(range(100_000, 1_000_000))


def get_list_of_recovery_codes(num: int = 10) -> list:
    return [get_recovery_code() for _ in range(num)]


def bulk_create_recovery_codes(user, num: int = 10) -> list[RecoveryCode]:
    """Bulk Create recovery codes for a user

    :param user: User object
    :param num: Recovery codes to generate, defaults to 10
    :return: list of RecoveryCode objects

    > This function doesn't handle any exceptions
    """

    codes = get_list_of_recovery_codes(num)

    recovery_codes = [RecoveryCode(user=user, code=code, used_at=None) for code in codes]

    return RecoveryCode.objects.bulk_create(recovery_codes)
