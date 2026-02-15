from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Post


class AuthenticationTests(TestCase):
	def test_register_creates_user_with_email_and_redirects(self):
		response = self.client.post(
			reverse('register'),
			{
				'username': 'alice',
				'email': 'alice@example.com',
				'password1': 'StrongPass123!@#',
				'password2': 'StrongPass123!@#',
			},
		)
		self.assertEqual(response.status_code, 302)
		user = User.objects.get(username='alice')
		self.assertEqual(user.email, 'alice@example.com')

	def test_profile_requires_login(self):
		response = self.client.get(reverse('profile'))
		self.assertEqual(response.status_code, 302)
		self.assertIn('/login/', response['Location'])

	def test_profile_update_email(self):
		user = User.objects.create_user(
			username='bob',
			email='old@example.com',
			password='StrongPass123!@#',
		)
		self.client.login(username='bob', password='StrongPass123!@#')

		response = self.client.post(
			reverse('profile'),
			{
				'username': 'bob',
				'first_name': 'Bob',
				'last_name': 'Builder',
				'email': 'new@example.com',
			},
		)
		self.assertEqual(response.status_code, 302)
		user.refresh_from_db()
		self.assertEqual(user.email, 'new@example.com')


class PostCrudTests(TestCase):
	def setUp(self):
		self.author = User.objects.create_user(
			username='author',
			email='author@example.com',
			password='StrongPass123!@#',
		)
		self.other_user = User.objects.create_user(
			username='other',
			email='other@example.com',
			password='StrongPass123!@#',
		)
		self.post = Post.objects.create(
			title='Hello',
			content='World',
			author=self.author,
		)

	def test_post_list_is_public(self):
		response = self.client.get(reverse('post-list'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Hello')

	def test_post_detail_is_public(self):
		response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'World')

	def test_create_requires_login(self):
		response = self.client.get(reverse('post-create'))
		self.assertEqual(response.status_code, 302)
		self.assertIn('/login/', response['Location'])

	def test_create_sets_author_to_logged_in_user(self):
		self.client.login(username='other', password='StrongPass123!@#')
		response = self.client.post(
			reverse('post-create'),
			{'title': 'New', 'content': 'Post'},
		)
		self.assertEqual(response.status_code, 302)
		created = Post.objects.get(title='New')
		self.assertEqual(created.author, self.other_user)

	def test_update_forbidden_for_non_author(self):
		self.client.login(username='other', password='StrongPass123!@#')
		response = self.client.get(
			reverse('post-update', kwargs={'pk': self.post.pk})
		)
		self.assertEqual(response.status_code, 403)

	def test_delete_forbidden_for_non_author(self):
		self.client.login(username='other', password='StrongPass123!@#')
		response = self.client.post(
			reverse('post-delete', kwargs={'pk': self.post.pk})
		)
		self.assertEqual(response.status_code, 403)
		self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())
