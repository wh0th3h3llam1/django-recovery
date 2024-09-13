from django.contrib import admin

from .models import RecoveryCode


class RecoveryCodeAdmin(admin.ModelAdmin):

    list_display = ("code", "user", "used", "used_at")
    list_filter = ("used", "used")


admin.site.register(RecoveryCode, RecoveryCodeAdmin)
