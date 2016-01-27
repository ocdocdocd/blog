from django.db import models
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager


class BlogPost(models.Model):
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=64)
    pubDate = models.DateField()
    slug = models.SlugField(max_length=128)
    body = models.TextField()
    summary = models.TextField()
    categories = TaggableManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.summary = self.body[:1000]
        super(BlogPost, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class Images(models.Model):
    img = models.ImageField()
    post = models.ForeignKey(BlogPost)
