from django.contrib import admin

from .models import BlogPost, Comment, Images, UserLikes


class ImagesInline(admin.StackedInline):
    model = Images


class BlogPostAdmin(admin.ModelAdmin):
    inlines = [ImagesInline, ]

admin.site.register(Comment)
admin.site.register(BlogPost, BlogPostAdmin)
