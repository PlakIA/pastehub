from django.db import models
from django.utils.translation import gettext_lazy as _

from paste.models import Paste
from users.models import CustomUser


class Person(models.Model):
    name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name=_("имя"),
        help_text=_("Как к вам обращаться?"),
    )
    email = models.EmailField(
        verbose_name=_("почта"),
        help_text=_("Адрес электронной почты для обратной связи"),
    )

    class Meta:
        verbose_name = _("персональные данные")
        verbose_name_plural = _("персональные данные")

    def __str__(self):
        return f"{self.name} ({self.email})"


class Report(models.Model):
    statuses = [
        ("new", _("Получено")),
        ("wip", _("В работе")),
        ("approved", _("Принято")),
        ("rejected", _("Отклонено")),
    ]

    paste = models.ForeignKey(
        Paste,
        on_delete=models.CASCADE,
        related_name="reports",
        related_query_name="report",
        verbose_name=_("паста"),
    )
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        related_name="report",
        verbose_name=_("отправитель"),
    )
    status = models.CharField(
        choices=statuses,
        max_length=10,
        default="new",
        verbose_name=_("статус"),
    )
    text = models.TextField(
        verbose_name=_("текст жалобы"),
        help_text=_("Опишите нарушение"),
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("нарушение")
        verbose_name_plural = _("нарушения")

    def __str__(self):
        return str(self.id)


class ReportReview(models.Model):
    statuses = [
        ("new", _("Получено")),
        ("wip", _("В работе")),
        ("approved", _("Принято")),
        ("rejected", _("Отклонено")),
    ]

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="report_review",
        verbose_name=_("автор пасты"),
    )
    paste = models.ForeignKey(
        Paste,
        on_delete=models.CASCADE,
        related_name="report_review",
        verbose_name=_("паста"),
    )
    status = models.CharField(
        choices=statuses,
        max_length=10,
        default="new",
        verbose_name=_("статус"),
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("пересмотр нарушения")
        verbose_name_plural = _("пересмотры нарушений")

    def __str__(self):
        return str(self.id)


__all__ = ["Report", "Person", "ReportReview"]
