from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Author, Book


class BookViewsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author,
        )

        User = get_user_model()
        self.user = User.objects.create_user(username="tester", password="pass12345")

    def test_list_is_public(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_is_public(self):
        url = reverse("book-detail", kwargs={"pk": self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_requires_auth(self):
        url = reverse("book-create")
        response = self.client.post(
            url,
            {"title": "New Book", "publication_year": 2021, "author": self.author.pk},
            format="json",
        )
        self.assertIn(response.status_code, (401, 403))

    def test_create_rejects_future_publication_year(self):
        url = reverse("book-create")
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            url,
            {"title": "Future Book", "publication_year": 9999, "author": self.author.pk},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_create_succeeds_when_authenticated(self):
        url = reverse("book-create")
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            url,
            {"title": "New Book", "publication_year": 2021, "author": self.author.pk},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
