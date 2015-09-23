from django.conf.urls import patterns, url, include
from blog import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^post/(?P<blog_post_slug>[\w\-]+)/$', views.blog_post, name='post'),
                       url(r'^get_entries/', views.get_entries, name="get_entries"),
                       url(r'^archive/(?P<archive_slug>[\w\-]+)/$', views.archive, name='archive'),
                       url(r'^category/(?P<cat_slug>[\w\-]+)/$', views.category, name='category'),
                       url(r'^tinymce/', include('tinymce.urls')),
                       )
