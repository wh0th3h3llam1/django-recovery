from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


RECOVERY_CODE_LENGTH = getattr(settings, "RECOVERY_CODE_LENGTH", 8)

if RECOVERY_CODE_LENGTH not in range(8, 17):
    raise ImproperlyConfigured("RECOVERY_CODE_LENGTH must be between `8` and `16`")
