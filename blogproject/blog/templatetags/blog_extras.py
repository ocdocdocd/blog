from django import template
from django.template.defaultfilters import slugify
from blog.models import BlogPost
from taggit.models import Tag

register = template.Library()


@register.inclusion_tag('blog/archive_template.html')
def print_dates():
    dates = []
    archives = []
    posts = BlogPost.objects.all().order_by('-pubDate')
    for post in posts:
        date = post.pubDate.strftime("%B %Y")
        if date not in dates:
            dates.append(date)
            archives.append((date, slugify(date)))
    context_dict = {'archives': archives}
    return context_dict


@register.inclusion_tag('blog/cat_template.html')
def print_categories():
    categories = Tag.objects.all()
    cats = []
    for cat in categories:
        cats.append((cat, slugify(cat)))
    context_dict = {'cats': cats}
    return context_dict
