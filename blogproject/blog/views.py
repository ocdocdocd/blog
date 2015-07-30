from django.shortcuts import render
from blog.models import BlogPost, Comment
from blog.forms import userForm, blogForm, commentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from django.core.serializers import serialize


def index(request):
    posts = BlogPost.objects.order_by('-pubDate')

    context_dict = {'posts': posts}
    return render(request, 'blog/index.html', context_dict)


def blogPost(request, blog_post_slug):
    context_dict = {}

    try:
        post = BlogPost.objects.get(slug=blog_post_slug)
        comments = Comment.objects.filter(parent=post)

        context_dict['post'] = post
        context_dict['comments'] = comments
        context_dict['num_comments'] = len(comments)

    except BlogPost.DoesNotExist:
        pass

    return render(request, 'blog/post.html', context_dict)


def register(request):
    context_dict = {}

    if request.method == "POST":
        form = userForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()

            return index(request)

    else:
        form = userForm()

    context_dict['form'] = form
    return render(request, 'blog/register.html', context_dict)


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('user')
        password = request.POST.get('pass')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return index(request)
            else:
                return HttpResponse("Your account is disabled")
        else:
            return HttpResponse("Invalid login details")
    else:
        return render(request, 'blog/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return index(request)


@login_required
def post_comment(request):
    slug = request.path_info.split('/')[-2]
    parent_post = BlogPost.objects.get(slug=slug)
    user = request.user.get_username()
    today = timezone.now()
    comment = request.POST.get('post_comment')

    posted_comment = Comment(parent_post, user, today, comment)
    posted_comment.save()

    return HttpResponse(serialize('json', posted_comment))
