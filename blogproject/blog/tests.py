import datetime
import factory
import factory.fuzzy
import random
import string

from blog.models import BlogPost
from blog.templatetags.blog_extras import print_dates
from django.core.urlresolvers import reverse
from django.test import TestCase


def random_string(length=10):
    return u''.join(random.choice(string.ascii_letters) for x in range(length))


class BlogPostFactory(factory.DjangoModelFactory):
    class Meta:
        model = BlogPost

    title = random_string(random.randint(5, 50))
    author = random_string(random.randint(5, 20))
    pubDate = factory.fuzzy.FuzzyDate(datetime.date(2013, 1, 1))
    body = random_string(random.randint(400, 2500))

    @factory.post_generation
    def cats(self, create, extracted, **kwargs):
        if extracted and type(extracted) == list:
            for cat in extracted:
                self.categories.add(cat)
        else:
            self.categories.add('a', 'b', 'c')


class TestBlogViews(TestCase):

    def test_archive(self):
        '''
        Tests that archive view works.
        '''
        BlogPostFactory.create_batch(20)
        context = print_dates()
        dates = context['archives']

        # Test that archive() succeeds for dates that have posts
        found_posts = 0
        for date in dates:
            resp = self.client.get(reverse('archive',
                                           kwargs={'archive_slug': date[1]}))
            posts = resp.context['posts']
            self.assertFalse(len(posts) == 0)
            found_posts += len(posts)

        self.assertEqual(20, found_posts)

        # Test that archive() returns empty page for dates that have no posts
        resp = self.client.get(reverse('archive',
                                       kwargs={'archive_slug': 'July-2012'}))
        self.assertEqual(len(resp.context['posts']), 0)
        self.assertContains(resp, 'No results found.', 1)

        # Test that invalid input is returned with an error
        resp = self.client.get(reverse('archive',
                                       kwargs={'archive_slug': 'July'}))
        self.assertContains(resp, "There was an error", 1)

    def test_blog_post(self):
        '''
        Tests the blog_post view.
        '''
        BlogPostFactory.create(title='test post')
        # Test getting a post that exists
        resp = self.client.get(reverse('post',
                                       kwargs={'blog_post_slug': 'test-post'}))
        # Title of post should be rendered twice in page
        self.assertContains(resp, 'test post', 2)

        # Test getting a post that doesn't exist
        resp = self.client.get(reverse('post',
                                       kwargs={'blog_post_slug': 'derp'}))
        self.assertFalse('post' in resp.context)

    def test_category(self):
        '''
        Tests the category view.
        '''
        BlogPostFactory.create(title='post1', cats=['test'])
        BlogPostFactory.create(title='post2', cats=['test', 'test2'])
        BlogPostFactory.create(title='post3', cats=[])
        BlogPostFactory.create_batch(8)

        # test on an input that should return 2 results, post1 and post2
        resp = self.client.get(reverse('category',
                                       kwargs={'cat_slug': 'test'}))
        self.assertEqual(len(resp.context['posts']), 2)
        # the page will contain 2 hits for each title due to the URL slug
        self.assertContains(resp, 'post1', 2)
        self.assertContains(resp, 'post2', 2)

        # test on an input that should return no results
        resp = self.client.get(reverse('category',
                                       kwargs={'cat_slug': 'foo'}))
        self.assertEqual(len(resp.context['posts']), 0)
        self.assertContains(resp, "No results found.", 1)

        # test on an input that will become blank after processing
        resp = self.client.get(reverse('category',
                                       kwargs={'cat_slug': '-'}))
        self.assertEqual(len(resp.context['posts']), 0)
        self.assertContains(resp, "No results found.", 1)

    def test_get_entries_with_posts(self):
        '''
        Tests the get_entries() view with posts.
        '''
        BlogPostFactory.create_batch(12)
        # Test getting first page of extra posts
        resp = self.client.post(reverse('get_entries'),
                                {'page_num': 1})
        posts = resp.context['posts']
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(posts), 5)

        # Test getting second page of extra posts which should return
        # only two posts instead of five
        resp = self.client.post(reverse('get_entries'),
                                {'page_num': 2})
        posts = resp.context['posts']
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(posts), 2)

        # Test getting non-existent page of extra posts which should
        # return nothing
        resp = self.client.post(reverse('get_entries'),
                                {'page_num': 3})
        posts = resp.context['posts']
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(posts), 0)

    def test_get_entries_with_no_posts(self):
        '''
        Tests the get_entries() view with no posts.
        '''
        resp = self.client.post(reverse('get_entries'),
                                {'page_num': 1})
        posts = resp.context['posts']
        self.assertEqual(len(posts), 0)
        self.assertContains(resp, '', 1)

    def test_index_with_posts(self):
        '''
        Tests that index page is correctly rendered with blog posts.
        '''
        # Test that fewer than 5 posts works
        BlogPostFactory.create_batch(3)
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('posts' in resp.context)
        posts = resp.context['posts']
        self.assertEqual(len(posts), 3)

        # Test that only 5 posts are returned at first
        BlogPostFactory.create_batch(6)
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('posts' in resp.context)
        posts = resp.context['posts']
        self.assertEqual(len(posts), 5)

    def test_index_with_no_posts(self):
        '''
        Test that index page is correctly rendered with no blog posts.
        '''
        resp = self.client.get(reverse('index'))
        self.assertContains(resp, "There aren't any blog posts yet!", 1)
