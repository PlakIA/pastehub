from django.conf import settings
from django.test import TestCase

from paste.models import Category, Paste


class TestModel(TestCase):
    def tearDown(self):
        Paste.objects.all().delete()

    def test_create_paste(self):
        pastes_count = Paste.objects.count()
        test_paste = Paste.objects.create(title="Test Title")

        self.assertEqual(Paste.objects.count(), pastes_count + 1)
        self.assertEqual(
            len(test_paste.short_link),
            settings.SHORT_LINK_LENGTH,
        )

    def test_create_category(self):
        categories_count = Category.objects.count()
        Category.objects.create(name="Test Category")

        self.assertEqual(Category.objects.count(), categories_count + 1)


__all__ = []
