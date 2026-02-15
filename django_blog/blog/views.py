from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import PostForm, UserRegistrationForm, UserUpdateForm
from .models import Post


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


class PostDetailView(DetailView):
	model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	form_class = PostForm

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def get_success_url(self):
		return reverse('post-detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	form_class = PostForm
	raise_exception = True

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

	def test_func(self):
		post = self.get_object()
		return post.author == self.request.user
