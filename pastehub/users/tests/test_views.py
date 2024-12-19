from django.test import Client, TestCase

import paste.models
import users.models


class UserPasteListTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.category = paste.models.Category.objects.create(
            name="test_category",
        )
        cls.author = users.models.CustomUser.objects.create(
            first_name="test",
            last_name="test",
            email="test@gmail.com",
            password="1234",
            username="test_user",
        )
        cls.pastes = []
        for i in range(3):
            cls.pastes.append(
                paste.models.Paste.objects.create(
                    title=f"test_paste{i}",
                    category=cls.category,
                    author=cls.author,
                ),
            )

    def test_correct_item_list(self):
        response = Client().get("/users/test_user/?page=1")
        self.assertIn("page_obj", response.context)

        for test_paste in self.pastes:
            self.assertIn(test_paste, response.context["page_obj"])
            self.assertEqual(test_paste.author, self.author)

        self.assertEqual(len(response.context["page_obj"]), len(self.pastes))

    def test_user_not_found(self):
        response = Client().get("/users/unknown_user/")
        self.assertEqual(response.status_code, 404)

    @classmethod
    def tearDown(cls):
        paste.models.Category.objects.all().delete()
        paste.models.Paste.objects.all().delete()
        users.models.CustomUser.objects.all().delete()


__all__ = ()
