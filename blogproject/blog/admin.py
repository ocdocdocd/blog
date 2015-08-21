from django.contrib import admin

from .models import BlogPost, Comment, Images, UserLikes


class ImagesInline(admin.StackedInline):
    model = Images


class BlogPostAdmin(admin.ModelAdmin):
    inlines = [ImagesInline, ]
    change_form_template = 'blog/admin/change_form.html'
    prepopulated_fields = {'slug': ('title',), 'summary': ('body',),}


admin.site.register(Comment)
admin.site.register(BlogPost, BlogPostAdmin)
