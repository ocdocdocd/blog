from django.shortcuts import render
from blog.models import BlogPost, Comment


def index(request):
    posts = BlogPost.objects.order_by('-pubDate')

    context_dict = {'posts': posts}
    response = render(request, 'blog/index.html', context_dict)
    return response

def blogPost(request, blog_post_slug):
    context_dict = {}

    try:
        post = BlogPost.objects.get(slug=blog_post_slug)
        comments = Comment.objects.filter(parent=post)

        context_dict['post'] = post
        context_dict['comments'] = comments

    except BlogPost.DoesNotExist:
        pass

    return render(request, 'blog/post.html', context_dict)
