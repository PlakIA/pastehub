from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    image = models.ImageField(
        verbose_name="аватарка",
        upload_to="uploads/profile_images/",
        help_text="Ваша аватарка",
        null=True,
        blank=True,
    )


__all__ = ()
