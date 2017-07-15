from django import forms

class SearchForm(forms.Form):
    search_text = forms.CharField(max_length=20, widget=forms.TextInput({
        'class': 'form-control'
    }))