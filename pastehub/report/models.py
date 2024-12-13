from django.db import models

from paste.models import Paste
from users.models import CustomUser


class Person(models.Model):
    name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="имя",
        help_text="Как к вам обращаться?",
    )
    email = models.EmailField(
        verbose_name="почта",
        help_text="Адрес электронной почты для обратной связи",
    )

    class Meta:
        verbose_name = "персональные данные"
        verbose_name_plural = "персональные данные"

    def __str__(self):
        return f"{self.name} ({self.email})"


class Report(models.Model):
    statuses = [
        ("new", "Получено"),
        ("wip", "В работе"),
        ("approved", "Принято"),
        ("rejected", "Отклонено"),
    ]

    paste = models.ForeignKey(
        Paste,
        on_delete=models.CASCADE,
        related_name="reports",
        related_query_name="report",
        verbose_name="паста",
    )
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        related_name="report",
        verbose_name="отправитель",
    )
    status = models.CharField(
        choices=statuses,
        max_length=10,
        default="new",
        verbose_name="статус",
    )
    text = models.TextField(
        verbose_name="текст жалобы",
        help_text="Опишите нарушение",
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "нарушение"
        verbose_name_plural = "нарушения"

    def __str__(self):
        return str(self.id)


class ReportReview(models.Model):
    statuses = [
        ("new", "Получено"),
        ("wip", "В работе"),
        ("approved", "Принято"),
        ("rejected", "Отклонено"),
    ]

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="report_review",
        verbose_name="автор пасты",
    )
    paste = models.ForeignKey(
        Paste,
        on_delete=models.CASCADE,
        related_name="report_review",
        verbose_name="паста",
    )
    status = models.CharField(
        choices=statuses,
        max_length=10,
        default="new",
        verbose_name="статус",
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "пересмотр нарушения"
        verbose_name_plural = "пересмотры нарушений"

    def __str__(self):
        return str(self.id)


__all__ = ["Report", "Person", "ReportReview"]
