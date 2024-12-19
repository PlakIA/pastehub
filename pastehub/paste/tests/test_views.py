import http
import shutil

from django.conf import settings
from django.test import override_settings, TestCase
from django.urls import reverse

from core.storage import upload_to_storage
from paste.models import Paste


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

    def tearDown(self):
        Paste.objects.all().delete()
        shutil.rmtree(settings.MEDIA_ROOT)

    def test_endpoint_create(self):
        response = self.client.get(reverse("paste:create"))

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTrue(response.context["form"])

<<<<<<< HEAD
    def test_correct_create_post(self):
        new_paste_data = {
            "title": "Test title1",
            "content": "Test content",
            "category": 1,
            "language": "text",
        }
        self.client.post(reverse("paste:create"), new_paste_data)

        self.assertEqual(
            len(os.listdir(settings.MEDIA_ROOT / "pastes")),
            3,
        )
        self.assertEqual(
            len(os.listdir(settings.MEDIA_ROOT / "pastes/versions/")),
            1,
        )

=======
>>>>>>> feature/api
    def test_endpoint_detail(self):
        response = self.client.get(
            reverse("paste:detail", args=(self.test_paste.short_link,)),
        )

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTrue(response.context["paste"])
        self.assertTrue(response.context["content"])

    def test_delete_redirect(self):
        response = self.client.get(
            reverse("paste:delete", args=(self.test_paste.short_link,)),
        )

        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            reverse("paste:detail", args=(self.test_paste.short_link,)),
        )


__all__ = []
