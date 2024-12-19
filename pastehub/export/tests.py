import http
import json
import shutil

from django.conf import settings
from django.test import override_settings, TestCase
from django.urls import reverse

from core.storage import upload_to_storage
from paste.models import Category, Paste, PasteVersion


__all__ = []


@override_settings(
    MEDIA_ROOT=settings.BASE_DIR / "media_test",
)
class TestViews(TestCase):
    def setUp(self):
        self.test_paste = Paste.objects.create(title="Test Paste")
        upload_to_storage(
            f"pastes/{self.test_paste.id}",
            "Lorem ipsum dolor sit amet...",
        )
        self.test_paste_version_1 = PasteVersion.objects.create(
            paste=self.test_paste,
            version=1,
            title=self.test_paste.title,
        )
        upload_to_storage(
            f"pastes/versions/{self.test_paste.id}_1",
            "Lorem ipsum dolor sit amet...",
        )

        self.category = Category.objects.create(name="Aboba")

    def tearDown(self):
        Paste.objects.all().delete()
        PasteVersion.objects.all().delete()
        shutil.rmtree(settings.MEDIA_ROOT)

    def test_positive_endpoint_export_source(self):
        response = self.client.get(
            reverse(
                "export:source",
                args=(
                    self.test_paste.short_link,
                    self.test_paste_version_1.version,
                ),
            ),
        )

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(
            response.get("Content-Disposition"),
            f"attachment; filename={self.test_paste.short_link}_"
            f"{self.test_paste_version_1.version}.txt",
        )
        self.assertEqual(
            response.get("content-type"),
            "text/plain",
        )

    def test_negative_endpoint_export_source(self):
        response = self.client.get(
            reverse(
                "export:source",
                args=(
                    "fsdfdsfdsf",
                    self.test_paste_version_1.version,
                ),
            ),
        )

        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND)

    def test_positive_endpoint_json_source(self):
        response = self.client.get(
            reverse(
                "export:json",
                args=(
                    self.test_paste.short_link,
                    self.test_paste_version_1.version,
                ),
            ),
        )

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(
            response.get("Content-Disposition"),
            f"attachment; filename={self.test_paste.short_link}_"
            f"{self.test_paste_version_1.version}.json",
        )
        self.assertEqual(
            json.loads(response.content),
            {
                "content": "Lorem ipsum dolor sit amet...",
                "title": self.test_paste.title,
                "author": str(self.test_paste.author),
                "category": str(self.test_paste.category),
                "created": self.test_paste.created.isoformat()[:-9] + "Z",
                "short_link": self.test_paste.short_link,
            },
        )
        self.assertEqual(
            response.get("content-type"),
            "application/json",
        )

    def test_negative_endpoint_json_source(self):
        response = self.client.get(
            reverse(
                "export:json",
                args=(
                    "fsdfdsfdsf",
                    self.test_paste_version_1.version,
                ),
            ),
        )

        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND)

    def test_positive_endpoint_export_markdown(self):
        response = self.client.get(
            reverse(
                "export:markdown",
                args=(
                    self.test_paste.short_link,
                    self.test_paste_version_1.version,
                ),
            ),
        )

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(
            response.get("Content-Disposition"),
            f"attachment; filename={self.test_paste.short_link}_"
            f"{self.test_paste_version_1.version}.md",
        )
        self.assertEqual(
            response.content.decode("utf-8"),
            "Lorem ipsum dolor sit amet...",
        )
        self.assertEqual(
            response.get("content-type"),
            "text/markdown",
        )

    def test_negative_endpoint_export_markdown(self):
        response = self.client.get(
            reverse(
                "export:markdown",
                args=(
                    "fsdfdsfdsf",
                    self.test_paste_version_1.version,
                ),
            ),
        )

        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND)
