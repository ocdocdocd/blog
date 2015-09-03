from django.contrib import admin
from django import forms
from django.db import models
from .models import BlogPost, Comment, Images
from tinymce.widgets import TinyMCE


class ImagesInline(admin.StackedInline):
    model = Images


class BlogPostAdmin(admin.ModelAdmin):
    inlines = [ImagesInline, ]
    prepopulated_fields = {'slug': ('title',), 'summary': ('body',), }
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows':30})},
    }


admin.site.register(Comment)
admin.site.register(BlogPost, BlogPostAdmin)
