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

    def test_update_requires_auth(self):
        url = reverse("book-update", kwargs={"pk": self.book.pk})
        response = self.client.patch(url, {"title": "Updated"}, format="json")
        self.assertIn(response.status_code, (401, 403))

    def test_update_succeeds_when_authenticated(self):
        url = reverse("book-update", kwargs={"pk": self.book.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"title": "Updated"}, format="json")
        self.assertEqual(response.status_code, 200)

        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated")

    def test_delete_requires_auth(self):
        url = reverse("book-delete", kwargs={"pk": self.book.pk})
        response = self.client.delete(url)
        self.assertIn(response.status_code, (401, 403))

    def test_delete_succeeds_when_authenticated(self):
        url = reverse("book-delete", kwargs={"pk": self.book.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertIn(response.status_code, (200, 202, 204))
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())

    def test_filtering_by_author(self):
        other_author = Author.objects.create(name="Other Author")
        Book.objects.create(title="Other Book", publication_year=2019, author=other_author)

        url = reverse("book-list")
        response = self.client.get(url, {"author": other_author.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Other Book")

    def test_search_by_title(self):
        Book.objects.create(title="A Searchable Title", publication_year=2018, author=self.author)

        url = reverse("book-list")
        response = self.client.get(url, {"search": "Searchable"})
        self.assertEqual(response.status_code, 200)
        titles = [item["title"] for item in response.data]
        self.assertIn("A Searchable Title", titles)

    def test_ordering_by_publication_year_desc(self):
        Book.objects.create(title="Old", publication_year=1999, author=self.author)
        Book.objects.create(title="New", publication_year=2023, author=self.author)

        url = reverse("book-list")
        response = self.client.get(url, {"ordering": "-publication_year"})
        self.assertEqual(response.status_code, 200)
        years = [item["publication_year"] for item in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
