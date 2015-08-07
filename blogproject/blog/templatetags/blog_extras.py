from django import template
from blog.models import UserLikes, BlogPost

register = template.Library()


@register.inclusion_tag('blog/comment_template.html')
def generate_comments(comment, user):
    isLiked = UserLikes.objects.get_or_create(user=user, comment=comment)[0]
    if isLiked.liked:
        btn_classes = "btn btn-success btn-xs likebtn liked"
    else:
        btn_classes = "btn btn-success btn-xs likebtn"
    context_dict = {"classes": btn_classes, "comment": comment}
    return context_dict


@register.inclusion_tag('blog/archive_template.html')
def print_dates():
    dates = []
    slugs = []
    posts = BlogPost.objects.all().order_by('-pubDate')
    for post in posts:
        date = post.pubDate.strftime("%B %Y")
        if date not in dates:
            dates.append(date)
    context_dict = {"dates": dates, "slugs": slugs}
    return context_dict
