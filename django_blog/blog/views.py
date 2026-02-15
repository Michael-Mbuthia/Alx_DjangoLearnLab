from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CommentForm, PostForm, UserRegistrationForm, UserUpdateForm
from .models import Comment, Post, Tag


def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.email = form.cleaned_data['email']
			user.save()
			login(request, user)
			messages.success(request, 'Registration successful. You are now logged in.')
			return redirect('profile')
	else:
		form = UserRegistrationForm()

	return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
	if request.method == 'POST':
		form = UserUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, 'Profile updated successfully.')
			return redirect('profile')
	else:
		form = UserUpdateForm(instance=request.user)

	return render(request, 'blog/profile.html', {'form': form})


class PostListView(ListView):
	model = Post
	context_object_name = 'posts'
	ordering = ['-published_date']
	template_name = 'blog/post_list.html'


class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/post_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['comments'] = self.object.comments.select_related('author').order_by('created_at')
		context['comment_form'] = CommentForm()
		return context


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	form_class = PostForm
	template_name = 'blog/post_form.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def get_success_url(self):
		return reverse('post-detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	form_class = PostForm
	raise_exception = True
	template_name = 'blog/post_form.html'

	def test_func(self):
		post = self.get_object()
		return post.author == self.request.user

	def form_valid(self, form):
		form.instance.author = self.get_object().author
		return super().form_valid(form)

	def get_success_url(self):
		return reverse('post-detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = reverse_lazy('post-list')
	raise_exception = True
	template_name = 'blog/post_confirm_delete.html'

	def test_func(self):
		post = self.get_object()
		return post.author == self.request.user


class CommentCreateView(LoginRequiredMixin, CreateView):
	model = Comment
	form_class = CommentForm

	def dispatch(self, request, *args, **kwargs):
		self.parent_post = Post.objects.get(pk=kwargs['post_id'])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		form.instance.post = self.parent_post
		form.instance.author = self.request.user
		return super().form_valid(form)

	def get_success_url(self):
		return reverse('post-detail', kwargs={'pk': self.parent_post.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Comment
	form_class = CommentForm
	raise_exception = True
	template_name = 'blog/comment_form.html'

	def test_func(self):
		comment = self.get_object()
		return comment.author == self.request.user

	def get_success_url(self):
		return reverse('post-detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Comment
	raise_exception = True
	template_name = 'blog/comment_confirm_delete.html'

	def test_func(self):
		comment = self.get_object()
		return comment.author == self.request.user

	def get_success_url(self):
		return reverse('post-detail', kwargs={'pk': self.object.post.pk})


class TaggedPostListView(ListView):
	model = Post
	context_object_name = 'posts'
	template_name = 'blog/tag_posts.html'

	def get_queryset(self):
		tag_name = self.kwargs['tag_name']
		return (
			Post.objects.filter(tags__name__iexact=tag_name)
			.select_related('author')
			.prefetch_related('tags')
			.order_by('-published_date')
			.distinct()
		)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['tag_name'] = self.kwargs['tag_name']
		return context


class PostByTagListView(ListView):
	model = Post
	context_object_name = 'posts'
	template_name = 'blog/tag_posts.html'

	def get_queryset(self):
		tag_slug = self.kwargs['tag_slug']
		return (
			Post.objects.filter(tags__slug=tag_slug)
			.select_related('author')
			.prefetch_related('tags')
			.order_by('-published_date')
			.distinct()
		)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		tag_slug = self.kwargs['tag_slug']
		tag = Tag.objects.filter(slug=tag_slug).first()
		context['tag'] = tag
		context['tag_name'] = tag.name if tag else tag_slug
		return context


class PostSearchView(ListView):
	model = Post
	context_object_name = 'posts'
	template_name = 'blog/search_results.html'

	def get_queryset(self):
		query = (self.request.GET.get('q') or '').strip()
		if not query:
			return Post.objects.none()

		return (
			Post.objects.filter(
				Q(title__icontains=query)
				| Q(content__icontains=query)
				| Q(tags__name__icontains=query)
			)
			.select_related('author')
			.prefetch_related('tags')
			.order_by('-published_date')
			.distinct()
		)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['query'] = (self.request.GET.get('q') or '').strip()
		return context
