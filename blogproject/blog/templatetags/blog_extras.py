from django import template
from django.template.defaultfilters import slugify
from blog.models import BlogPost

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
