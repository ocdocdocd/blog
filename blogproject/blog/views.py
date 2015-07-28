from django.shortcuts import render


def index(request):
    context_dict = {}

    response = render(request, 'blog/index.html', context_dict)
    return response
