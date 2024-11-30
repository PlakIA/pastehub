import os
import random
import string

from django.conf import settings


def generate_short_link(length=settings.SHORT_LINK_LENGTH):
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=length),
    )


def upload_to_storage(key, content):
    directory = settings.MEDIA_ROOT / os.path.dirname(key)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(settings.MEDIA_ROOT / key, "w", encoding="utf-8") as f:
        f.write(content)


def get_from_storage(key):
    with open(settings.MEDIA_ROOT / key, "r", encoding="utf-8") as f:
        return f.read()


def delete_from_storage(key):
    os.remove(settings.MEDIA_ROOT / key)


__all__ = [
    "generate_short_link",
    "upload_to_storage",
    "get_from_storage",
    "delete_from_storage",
]
