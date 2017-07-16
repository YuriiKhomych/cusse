from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=6,
                               max_length=10,
                               widget=forms.TextInput(attrs={'type': 'password'}))


class SignUpForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Please enter your first name'
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Please enter your last name'
    )
    email = forms.EmailField(max_length=254,
                             help_text='Input a valid email address')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'birthday', 'password1', 'password2',)
