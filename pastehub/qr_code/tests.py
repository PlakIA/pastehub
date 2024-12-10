import http

from django.test import TestCase
from django.urls import reverse

from paste.models import Category, Paste


class TestViews(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Тестовая категория",
        )
        self.category.full_clean()
        self.category.save()

        self.paste = Paste.objects.create(
            title="Тестовая паста",
            category=self.category,
            is_protected=False,
        )
        self.paste.full_clean()
        self.paste.save()

    def test_endpoint_qr_code_preview(self):
        response = self.client.get(
            reverse(
                "qr_code:preview",
                args=("test_qr_code_text",),
            ),
        )

        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_positive_endpoint_qr_code_download(self):
        response = self.client.get(
            reverse(
                "qr_code:download",
                args=(
                    "PNG",
                    "test_qr_code_text",
                ),
            ),
        )

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(
            response.get("Content-Disposition"),
            "attachment; filename=qr_code.png",
        )
        self.assertEqual(
            response.get("content-type"),
            "image/PNG",
        )

    def test_negative_endpoint_qr_code_download_format(self):
        response = self.client.get(
            reverse(
                "qr_code:download",
                args=(
                    "ABC",
                    f"http://127.0.0.1/{self.paste.short_link}",
                ),
            ),
        )

        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND)


__all__ = []
