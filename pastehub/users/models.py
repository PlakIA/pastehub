from django.contrib.auth.models import AbstractUser
from django.db import models
from sorl.thumbnail import get_thumbnail


class CustomUser(AbstractUser):
    image = models.ImageField(
        verbose_name="аватарка",
        upload_to="uploads/profile_images/",
        help_text="Ваша аватарка",
        null=True,
        blank=True,
    )

    def _get_avatar(self, geometry):
        return get_thumbnail(
            self.image,
            geometry,
            crop="center",
            quality=51,
        )

    def get_avatar_32x32(self):
        if self.image:
            return self._get_avatar("32x32")

        return None


__all__ = ["CustomUser"]
