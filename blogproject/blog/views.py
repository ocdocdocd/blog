import calendar
import datetime

from blog.models import BlogPost
from django.http import HttpResponse
from django.shortcuts import render, render_to_response


def archive(request, archive_slug):
    '''
    Renders a page with all blog posts for the month given by archive_slug.
    '''
    try:
        datestr = archive_slug.replace("-", " ")
        date = datetime.datetime.strptime(datestr, "%B %Y")
        last_day = calendar.monthrange(date.year, date.month)[1]
        start_date = datetime.date(date.year, date.month, date.day)
        end_date = datetime.date(date.year, date.month, last_day)
        posts = BlogPost.objects.filter(pubDate__range=(start_date, end_date))
        context_dict = {"posts": posts}

        return render(request, 'blog/results.html', context_dict)
    except:
        return HttpResponse("There was an error in processing your request")


def blog_post(request, blog_post_slug):
    '''
    Renders the full page for a blog post.
    '''
    context_dict = {}

    try:
        post = BlogPost.objects.get(slug=blog_post_slug)
        context_dict['post'] = post

    except BlogPost.DoesNotExist:
        pass

    return render(request, 'blog/post.html', context_dict)


def category(request, cat_slug):
    '''
    Renders all blog posts that belong to the category given by cat_slug.
    '''
    try:
        category = cat_slug.replace('-', ' ')
        posts = BlogPost.objects.filter(categories__name__in=[category])
        context_dict = {"posts": posts}

        return render(request, 'blog/results.html', context_dict)
    except:
        return HttpResponse("There was an error in processing your request")


def get_entries(request):
    '''
    Fetches 5 more blog posts to append to the page.

    Returns 5 blog posts in pre-formatted in HTML.
    '''
    page = int(request.POST.get('page_num'))
    start = page * 5
    end = start + 5
    posts = BlogPost.objects.order_by('-pubDate')[start:end]
    context_dict = {'posts': posts}

    return render_to_response('blog/post_template.html', context_dict)


def index(request):
    '''
    Renders main page populated with the 5 most recent blog posts.
    '''
    posts = BlogPost.objects.order_by('-pubDate')[:5]

    context_dict = {'posts': posts}
    return render(request, 'blog/index.html', context_dict)
