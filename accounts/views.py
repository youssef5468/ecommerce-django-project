from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import LoginForm, ProfileForm, RegisterForm


def register_view(request):
    """Requirements 1-5: registration with full validation."""
    if request.user.is_authenticated:
        return redirect("catalog:home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend="accounts.backends.EmailAuthBackend")
            messages.success(request, "Welcome! Your account was created successfully.")
            return redirect("catalog:home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    """Requirement 6: log in using email and password."""
    if request.user.is_authenticated:
        return redirect("catalog:home")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user, backend="accounts.backends.EmailAuthBackend")
                next_url = request.GET.get("next") or "catalog:home"
                return redirect(next_url)
            form.add_error(None, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_view(request):
    """Requirement 7: log out."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("catalog:home")


@login_required
def profile_view(request):
    """Requirement 8: profile page after authentication."""
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/profile.html", {"form": form})
