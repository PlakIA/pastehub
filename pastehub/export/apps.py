from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ExportConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = _("Экспорт")


__all__ = ["ExportConfig"]
