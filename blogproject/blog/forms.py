from django import forms
from blog.models import BlogPost


class blogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'body']
