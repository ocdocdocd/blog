from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^post/(?P<blog_post_slug>[\w\-]+)/$', views.blogPost, name='post'),
                       )
