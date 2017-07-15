from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=6,
                               max_length=10,
                               widget=forms.TextInput(attrs={'type': 'password'}))
