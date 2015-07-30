from django import forms
from django.contrib.auth.models import User
from blog.models import BlogPost, Comment


class commentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', ]


class blogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'body']


class userForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
