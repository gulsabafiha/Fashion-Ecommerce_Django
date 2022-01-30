from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from .models import Billing_details, User


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'first_name': 'First Name',
                  'last_name': 'Last Name', 'email': 'Email'}

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})}


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control'}))


class CheckOutForm(forms.Form):
    class Meta:
        model = Billing_details

    first_name = forms.CharField(label=_(
        "First Name"), strip=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label=_(
        "Last Name"), strip=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    street_address = forms.CharField(label=_(
        "Street address"), strip=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apartments = forms.CharField(label=_(
        ""), strip=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    town_City = forms.CharField(label=_(
        "Town/City"), strip=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state_Country = forms.CharField(label=_(
        "State/Country"), strip=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    postcode_zip = forms.CharField(label=_(
        "Postcode/ZIP"), strip=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label=_("Phone"), strip=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.CharField(label=_("Email address"), strip=False,
                            widget=forms.EmailInput(attrs={'class': 'form-control'}))
