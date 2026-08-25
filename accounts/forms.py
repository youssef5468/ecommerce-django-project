from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import User


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={"class": "input"}))
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={"class": "input"}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "input"}))
    phone_number = forms.CharField(
        max_length=20, required=True,
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "01012345678"}),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone_number", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "input"})
        self.fields["password2"].widget.attrs.update({"class": "input"})

    def clean_email(self):
        # Requirement 3: email must be unique.
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        # username isn't shown to the user; email doubles as the unique login,
        # so we mirror it into username to satisfy Django's internal constraint.
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "input"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input"}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "input"}),
            "last_name": forms.TextInput(attrs={"class": "input"}),
            "phone_number": forms.TextInput(attrs={"class": "input"}),
        }
