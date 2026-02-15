from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
	name = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(max_length=60, unique=True, blank=True)

	def save(self, *args, **kwargs):
		if not self.slug:
			base = slugify(self.name)[:50] or 'tag'
			slug = base
			suffix = 2
			while Tag.objects.filter(slug=slug).exclude(pk=self.pk).exists():
				slug = f"{base}-{suffix}"
				suffix += 1
			self.slug = slug
		super().save(*args, **kwargs)

	def __str__(self):
		return self.name


class Post(models.Model):
	title = models.CharField(max_length=200)
	content = models.TextField()
	published_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='posts',
	)
	tags = models.ManyToManyField(Tag, related_name='posts', blank=True)


class Comment(models.Model):
	post = models.ForeignKey(
		Post,
		on_delete=models.CASCADE,
		related_name='comments',
	)
	author = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='comments',
	)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
