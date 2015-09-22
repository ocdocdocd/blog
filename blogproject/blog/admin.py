from django.contrib import admin
from django.db import models
from .models import BlogPost, Images
from tinymce.widgets import TinyMCE


class ImagesInline(admin.StackedInline):
    model = Images


class BlogPostAdmin(admin.ModelAdmin):
    inlines = [ImagesInline, ]
    prepopulated_fields = {'slug': ('title',), 'summary': ('body',), }
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }


admin.site.register(BlogPost, BlogPostAdmin)
