from django.apps import AppConfig


class RecoveryConfig(AppConfig):
    name = "recovery"
    verbose_name = "Recovery"
    default = True


class AutodiscoverRecoveryConfig(RecoveryConfig):
    default = False

    def ready(self):
        from django.utils.module_loading import autodiscover_modules

        autodiscover_modules("recovery")
