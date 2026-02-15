from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import UserRegistrationForm, UserUpdateForm


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
