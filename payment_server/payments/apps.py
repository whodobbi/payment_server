from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "payments"

    def ready(self) -> None:
        import payments.signals  # noqa: F401
        import payments.classic_site
        import payments.unfold_admin
