import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogproject.settings')

import django
django.setup()

from django.utils.text import slugify
import django.utils.timezone as timezone
import datetime

import random
from blog.models import BlogPost, Comment

def addBlogPost(title, author, date):
    p = BlogPost.objects.get_or_create(title=title)[0]
    p.author = author
    p.pubDate = date
    p.slug = slugify(title)

    body = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc tincidunt vestibulum rutrum. Sed lobortis molestie ipsum a dignissim. Cras non nibh ac metus ornare auctor in ut orci. Proin nibh neque, tincidunt convallis enim sit amet, laoreet varius ipsum. Ut tincidunt interdum arcu. In hac habitasse platea dictumst. Donec scelerisque ligula non interdum ultrices. Etiam sagittis bibendum ullamcorper. Aenean risus velit, dictum id erat non, egestas aliquet dui. Sed congue blandit hendrerit. Sed elementum ac metus nec aliquet. Proin nec cursus sapien. Suspendisse consectetur mattis lorem sit amet porttitor. Donec quis euismod elit. Phasellus mattis vulputate posuere. Quisque sagittis maximus lacus sit amet condimentum.

Aliquam accumsan mi bibendum lacus finibus, ultrices accumsan nibh eleifend. Nam vestibulum iaculis felis, sit amet mattis arcu. Quisque luctus nulla eu accumsan hendrerit. Fusce et ultricies neque, vel pellentesque tellus. Suspendisse eu consectetur purus. Mauris tincidunt pulvinar convallis. Ut semper sem quis quam porta dictum sed vulputate nibh. Fusce iaculis sollicitudin felis, id aliquet ligula sollicitudin vitae. Nunc cursus posuere purus non blandit. Duis eget augue ipsum. Maecenas cursus tortor vitae tellus suscipit porttitor. Mauris justo risus, commodo ut sem at, maximus ultricies erat. Mauris ac elit rutrum, pretium neque non, pharetra turpis.

Ut posuere ipsum eget volutpat rhoncus. Nullam sed vehicula urna. Curabitur faucibus erat non leo tincidunt, ut porttitor dui venenatis. Donec mollis erat ligula, non ullamcorper lacus aliquam et. Vivamus blandit ligula orci, eget mattis odio pharetra a. Donec vulputate urna feugiat, tincidunt lorem eu, aliquam sem. Aenean tempor ante et varius facilisis. Quisque in ante imperdiet, lobortis nulla vitae, vestibulum orci. Pellentesque lobortis nisi a mauris accumsan, id varius justo maximus.

Praesent nec bibendum velit. Nam et enim euismod, euismod tellus ac, commodo sapien. Cras luctus et dolor et ornare. Suspendisse dignissim mattis nibh sed finibus. Praesent congue fringilla metus nec commodo. Vestibulum tincidunt massa nec nunc hendrerit bibendum. Praesent consectetur odio in mauris ultrices venenatis. Nulla lobortis mi leo, sed porttitor massa imperdiet vel. Etiam dignissim id nisi a consequat.

Donec rutrum placerat tincidunt. Donec nisl ex, vulputate volutpat pulvinar non, tempor non risus. Curabitur id blandit eros. Vestibulum et nibh quis orci elementum molestie in sed nisi. Ut arcu dolor, lobortis a sem non, rhoncus viverra nisi. Sed sed erat sed purus placerat aliquet. Curabitur quis felis ullamcorper, scelerisque eros et, elementum nibh. Cras at enim sed nisi malesuada cursus. Sed in neque ac odio ullamcorper dictum. Donec sagittis libero eu ante ornare, ut fermentum eros ultrices.'''

    p.body = body
    p.summary = body[:500]
    p.likes = random.randint(0, 100)
    p.save()

    return p


def addComment(blogPost, author, pubDate):
    c1 = "Wow what a great post!"
    c2 = "These comments are kinda repetitive..."
    c3 = "Intredasting"
    c4 = "I'm commenting!"
    c5 = "How do I comment?"

    c = Comment.objects.get_or_create(parent=blogPost, pubDate=pubDate)[0]

    c.author = author
    comments = [c1, c2, c3, c4, c5]
    c.body = comments[random.randint(0, 4)]
    c.likes = random.randint(0, 50)
    c.save()

    return c


def populate():
    post1 = addBlogPost("The first post", "me", timezone.now())
    post2 = addBlogPost("The second post", "metoo", timezone.now())
    post3 = addBlogPost("The third Post", "me", timezone.now())

    posts = [post1, post2, post3]
    for p in posts:
        addComment(p, "anonymous", timezone.now())

    print "Finished populating database"

if __name__ == "__main__":
    print "Starting population script..."
    populate()
