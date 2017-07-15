from django.contrib import admin
from django import forms

from blog.models import Article

from redactor.widgets import RedactorEditor


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'image', 'author', 'liked_by']
        widgets = {
           'body': RedactorEditor(),
        }


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm


admin.site.register(Article, ArticleAdmin)
