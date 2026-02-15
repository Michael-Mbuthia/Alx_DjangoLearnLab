from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


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
