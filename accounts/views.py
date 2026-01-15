from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.views import View


class LoginView(View):
    """Handle user login."""
    template_name = 'accounts/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('chat:chat')
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('chat:chat')
        messages.error(request, "Invalid username or password.")
        return render(request, self.template_name, {'form': form})


class RegisterView(View):
    """Handle user registration."""
    template_name = 'accounts/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('chat:chat')
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('chat:chat')
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    """Handle user logout."""

    def get(self, request):
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect('accounts:login')

    def post(self, request):
        return self.get(request)
