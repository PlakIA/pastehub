from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from paste.models import Paste


class TestApi(TestCase):

    @classmethod
    def setUp(cls):
        cls.client = Client()

    def test_correct_root_endpoint(self):
        response = self.client.get(reverse("api:root"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_correct_paste_create(self):
        paste_count = Paste.objects.count()
        data = {"title": "test", "content": "print('hello world')"}
        response = self.client.post(reverse("api:paste-list"), data=data)

        self.assertEqual(paste_count + 1, Paste.objects.count())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


__all__ = ()
