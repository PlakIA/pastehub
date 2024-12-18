from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class QrCodeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "qr_code"
    verbose_name = _("QR Код")


__all__ = ["QrCodeConfig"]
