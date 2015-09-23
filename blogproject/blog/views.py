import calendar
import datetime
from django.shortcuts import render, render_to_response
from blog.models import BlogPost
from django.http import HttpResponse


def index(request):
    posts = BlogPost.objects.order_by('-pubDate')[:5]

    context_dict = {'posts': posts}
    return render(request, 'blog/index.html', context_dict)


def get_entries(request):
    page = int(request.POST.get('page_num'))
    start = page * 5
    end = start + 5
    posts = BlogPost.objects.order_by('-pubDate')[start:end]
    context_dict = {'posts': posts}

    return render_to_response('blog/post_template.html', context_dict)


def blog_post(request, blog_post_slug):
    context_dict = {}

    try:
        post = BlogPost.objects.get(slug=blog_post_slug)
        context_dict['post'] = post

    except BlogPost.DoesNotExist:
        pass

    return render(request, 'blog/post.html', context_dict)


def archive(request, archive_slug):
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


def category(request, cat_slug):
    try:
        category = cat_slug.replace('-', ' ')
        posts = BlogPost.objects.filter(categories__name__in=[category])
        context_dict = {"posts": posts}

        return render(request, 'blog/results.html', context_dict)
    except:
        return HttpResponse("There was an error in processing your request")
