from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^post/(?P<blog_post_slug>[\w\-]+)/$', views.blogPost, name='post'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       )
