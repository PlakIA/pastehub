import random
import string

from django.conf import settings


def generate_short_link(length=settings.SHORT_LINK_LENGTH):
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=length),
    )


__all__ = ["generate_short_link"]
