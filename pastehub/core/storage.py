import os

from django.conf import settings


def upload_to_storage(key, content):
    directory = settings.MEDIA_ROOT / os.path.dirname(key)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(settings.MEDIA_ROOT / key, "w", encoding="utf-8") as f:
        f.writelines(content)


def get_from_storage(key):
    with open(settings.MEDIA_ROOT / key, "r", encoding="utf-8") as f:
        return f.read()


def delete_from_storage(key):
    os.remove(settings.MEDIA_ROOT / key)


__all__ = [
    "upload_to_storage",
    "get_from_storage",
    "delete_from_storage",
]
