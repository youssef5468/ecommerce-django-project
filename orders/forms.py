from django import forms


class CheckoutForm(forms.Form):
    """Requirement 43: shipping information entered at checkout."""
    full_name = forms.CharField(max_length=200, label="Full name", widget=forms.TextInput(attrs={"class": "input"}))
    phone = forms.CharField(max_length=20, label="Phone number", widget=forms.TextInput(attrs={"class": "input"}))
    address = forms.CharField(max_length=255, label="Shipping address", widget=forms.TextInput(attrs={"class": "input"}))
    city = forms.CharField(max_length=100, label="City", widget=forms.TextInput(attrs={"class": "input"}))
