import uuid

from django.conf import settings
from django.db import models

from core.utils import generate_short_link


class Category(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="категория",
        help_text="Максимальная длинна 150 символов",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Paste(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        max_length=150,
        verbose_name="заголовок",
        help_text="Максимальная длинна 150 символов",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="pastes",
        related_query_name="paste",
        verbose_name="категория",
        null=True,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="pastes",
        related_query_name="paste",
        verbose_name="автор",
    )
    short_link = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="короткая ссылка",
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="опубликовано?",
    )
    is_protected = models.BooleanField(
        default=False,
        verbose_name="Зашифровано?",
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="обновлён")

    class Meta:
        verbose_name = "паста"
        verbose_name_plural = "пасты"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.short_link:
            self.short_link = generate_short_link()

        super().save(*args, **kwargs)


__all__ = ["Category", "Paste"]
