from django.db import models
from django.template.defaultfilters import slugify


class BlogPost(models.Model):
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=64)
    pubDate = models.DateField()
    slug = models.SlugField()
    body = models.TextField()
    summary = models.TextField()
    likes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    parent = models.ForeignKey(BlogPost)
    author = models.CharField(max_length=64)
    pubDate = models.DateField()
    body = models.TextField()
    likes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.author + ' - ' + str(self.pubDate)
