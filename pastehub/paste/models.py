from datetime import timedelta
import uuid

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.utils import generate_short_link

LANGUAGE_CHOICES = [
    ("markup", "Markup"),
    ("css", "CSS"),
    ("clike", "C-like"),
    ("javascript", "JavaScript"),
    ("python", "Python"),
    ("java", "Java"),
    ("csharp", "C#"),
    ("cpp", "C++"),
    ("php", "PHP"),
    ("ruby", "Ruby"),
    ("swift", "Swift"),
    ("go", "Go"),
    ("bash", "Bash"),
    ("sql", "SQL"),
    ("html", "HTML"),
    ("xml", "XML"),
    ("json", "JSON"),
    ("yaml", "YAML"),
    ("typescript", "TypeScript"),
    ("rust", "Rust"),
    ("kotlin", "Kotlin"),
    ("dart", "Dart"),
    ("scala", "Scala"),
    ("shell", "Shell"),
    ("powershell", "PowerShell"),
    ("haskell", "Haskell"),
    ("elixir", "Elixir"),
    ("text", "Plain Text"),
]
LANGUAGE_CHOICES.sort(key=lambda x: x[1])


class Category(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name=_("категория"),
        help_text=_("Максимальная длинна 150 символов"),
    )

    class Meta:
        verbose_name = _("категория")
        verbose_name_plural = _("категории")

    def __str__(self):
        return self.name


class BasePasteModel(models.Model):
    EXPIRED_LIMIT = [
        (timedelta(seconds=10), _("10 секунд")),
        (timedelta(minutes=10), _("10 минут")),
        (timedelta(hours=1), _("1 час")),
        (timedelta(days=1), _("1 день")),
        (timedelta(days=5), _("5 дней")),
        (timedelta(days=10), _("10 дней")),
        (timedelta(days=30), _("30 дней")),
        (None, _("Бессрочно")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        max_length=150,
        verbose_name=_("заголовок"),
        help_text=_("Максимальная длинна 150 символов"),
    )
    short_link = models.CharField(
        max_length=10,
        unique=True,
        verbose_name=_("короткая ссылка"),
    )
    language = models.CharField(
        verbose_name=_("язык для подсветки"),
        help_text=_("Выберите язык для подсветки"),
        max_length=50,
        choices=LANGUAGE_CHOICES,
        default="text",
    )
    expired_duration = models.DurationField(
        choices=EXPIRED_LIMIT,
        default=timedelta(days=1),
        null=True,
        blank=True,
        verbose_name=_("срок существования пасты"),
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("создана"),
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_("обновлено"),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.short_link:
            while True:
                short_link = generate_short_link()
                if not Paste.objects.filter(short_link=short_link).exists():
                    self.short_link = short_link
                    break

        super().save(*args, **kwargs)

    def is_expired(self):
        if not self.expired_duration:
            return False

        return self.updated + self.expired_duration <= timezone.now()


class Paste(BasePasteModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="pastes",
        related_query_name="paste",
        verbose_name=_("категория"),
        null=True,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="pastes",
        related_query_name="paste",
        verbose_name=_("автор"),
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name=_("опубликовать"),
    )
    is_blocked = models.BooleanField(
        default=False,
        verbose_name=_("заблокировать"),
    )
    updated = models.DateTimeField(auto_now=True, verbose_name=_("обновлён"))

    class Meta:
        verbose_name = _("паста")
        verbose_name_plural = _("пасты")

    def save(self, *args, **kwargs):
        if not self.short_link:
            self.short_link = generate_short_link()

        super().save(*args, **kwargs)


class PasteVersion(models.Model):
    paste = models.ForeignKey(
        Paste,
        on_delete=models.CASCADE,
        verbose_name=_("паста"),
        related_name="versions",
        related_query_name="version",
    )
    version = models.IntegerField(verbose_name=_("номер версии"))
    title = models.CharField(
        max_length=150,
        verbose_name=_("заголовок"),
        help_text=_("Максимальная длинна 150 символов"),
    )

    updated = models.DateTimeField(auto_now=True, verbose_name=_("обновлён"))

    class Meta:
        verbose_name = _("версия пасты")
        verbose_name_plural = _("версии паст")

    def __str__(self):
        return f"{self.paste.title} v{self.version}"


class ProtectedPaste(BasePasteModel):
    EXPIRED_LIMIT = [
        (timedelta(seconds=10), _("10 секунд")),
        (timedelta(minutes=10), _("10 минут")),
        (timedelta(hours=1), _("1 час")),
        (timedelta(days=1), _("1 день")),
        (timedelta(days=5), _("5 дней")),
        (timedelta(days=10), _("10 дней")),
        (timedelta(days=30), _("30 дней")),
    ]
    expired_duration = models.DurationField(
        choices=EXPIRED_LIMIT,
        default=timedelta(days=1),
        null=True,
        blank=True,
        verbose_name=_("срок существования пасты"),
    )
    password = models.CharField(
        max_length=255,
        verbose_name=_("ключ шифрования"),
    )
    salt = models.BinaryField(verbose_name=_("соль"))
    nonce = models.BinaryField(verbose_name=_("nonce"))

    class Meta:
        verbose_name = _("зашифрованная паста")
        verbose_name_plural = _("зашифрованные пасты")

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


__all__ = ["Category", "Paste", "ProtectedPaste", "PasteVersion"]
