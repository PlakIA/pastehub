from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def upload_to_storage(key, content):
    return default_storage.save(key, ContentFile(content.encode("utf8")))


def get_from_storage(key):
    with default_storage.open(key, "rb") as f:
        return f.read().decode("utf-8")


def delete_from_storage(key):
    default_storage.delete(key)


__all__ = [
    "upload_to_storage",
    "get_from_storage",
    "delete_from_storage",
]
