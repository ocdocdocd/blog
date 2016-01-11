from django.test import TestCase
from django.core.urlresolvers import reverse
import factory
import factory.fuzzy
import random
import string
import datetime

from blog.models import BlogPost, Comment, UserLikes
from django.contrib.auth.models import User
from blog.forms import commentForm, blogForm, userForm
from blog.templatetags.blog_extras import print_dates


def random_string(length=10):
    return u''.join(random.choice(string.ascii_letters) for x in range(length))


class BlogPostFactory(factory.DjangoModelFactory):
    class Meta:
        model = BlogPost

    title = random_string(random.randint(5, 50))
    author = random_string(random.randint(5, 20))
    pubDate = factory.fuzzy.FuzzyDate(datetime.date(2013, 1, 1))
    body = random_string(random.randint(400, 2500))


class CommentFactory(factory.DjangoModelFactory):
    class Meta:
        model = Comment

    parent = factory.SubFactory(BlogPostFactory)
    author = random_string(random.randint(5, 20))
    pubDate = factory.fuzzy.FuzzyDate(datetime.date(2013, 1, 1))
    body = random_string(random.randint(1, 100))
    likes = random.randint(1, 500)


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user%d' % n)
    password = factory.Sequence(lambda n: 'pass%d' % n)


class UserLikesFactory(factory.DjangoModelFactory):
    class Meta:
        model = UserLikes

    user = factory.SubFactory(UserFactory)
    comment = factory.SubFactory(CommentFactory)
    liked = random.choice((True, False))


class TestBlogViews(TestCase):

    def test_index(self):
        BlogPostFactory.create_batch(7)
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('posts' in resp.context)
        posts = resp.context['posts']
        self.assertEqual(len(posts), 7)

    def test_logout_logged_in(self):
        User.objects.create_user(username='auser', password='apass')
        self.client.login(username='auser', password='apass')
        resp = self.client.get(reverse('logout'))
        self.assertContains(resp, "There aren't any blog posts yet!", 1)

    def test_login_not_logged_in(self):
        u = User.objects.create_user(username='disabled',
                                     password='disable')
        u.is_active = False
        u.save()
        User.objects.create_user(username='auser',
                                 password='apass')

        # test that log-in form returned on GET
        resp = self.client.get(reverse('login'))
        self.assertContains(resp, 'login_form', 1)

        # test that invalid login details rejected
        resp = self.client.post(reverse('login'), {'user': 'invalid',
                                                   'pass': 'invalid'})
        self.assertContains(resp, 'Invalid login details', 1)

        # test login with allowed user
        resp = self.client.post(reverse('login'), {'user': 'auser',
                                                   'pass': 'apass'})
        self.assertContains(resp, "There aren't any blog posts yet!", 1)
        self.client.logout()

        # test that disabled user rejected
        resp = self.client.post(reverse('login'), {'user': 'disabled',
                                                   'pass': 'disable'})
        self.assertContains(resp, 'Your account is disabled', 1)

    def test_login_logged_in(self):
        User.objects.create_user(username='auser',
                                 password='apass')
        self.client.login(username='auser', password='apass')
        resp = self.client.get(reverse('login'))
        self.assertContains(resp, "You are already logged in!", 1)

        resp = self.client.post(reverse('login'), {'user': 'auser',
                                                   'pass': 'apass'})
        self.assertContains(resp, "You are already logged in!", 1)

    def test_register_not_logged_in(self):
        # test that form can be obtained
        resp = self.client.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)
        form = resp.context['form']
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        self.assertIn('email', form.fields)

        # test that valid form is accepted and processed correctly
        # form['username'] = 'auser'
        # form['password'] = 'apass'
        # form['email'] = 'user@user.com'
        # resp = self.client.post('/blog/register', {'form': form}, follow=True)
        # self.assertEqual(resp.status_code, 200)
        # user = User.objects.get(username='auser')
        # self.assertEqual(user.username, 'auser')
        # self.assertEqual(user.email, 'user@user.com')

    def test_register_logged_in(self):
        User.objects.create_user(username='auser', password='apass')
        self.client.login(username='auser', password='apass')
        resp = self.client.get(reverse('register'))
        self.assertContains(resp, "You're already logged in!", 1)

        resp = self.client.post(reverse('register'))
        self.assertContains(resp, "You're already logged in!", 1)

    def test_blogPost_no_comments_not_logged_in(self):
        BlogPostFactory(title='The Post')

        resp = self.client.get('/blog/post/the-post', follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_blogPost_no_comments_logged_in(self):
        BlogPostFactory(title='The Post')
        User.objects.create_user(username='auser', password='apass')
        self.client.login(username='auser', password='apass')

        resp = self.client.get('/blog/post/the-post', follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_blogPost_with_comments_not_logged_in(self):
        post = BlogPostFactory(title='The Post')
        CommentFactory.create_batch(5, parent=post)

        resp = self.client.get('/blog/post/the-post', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['num_comments'], 5)

    def test_blogPost_with_comments_logged_in(self):
        post = BlogPostFactory(title='The Post')
        CommentFactory.create_batch(5, parent=post)
        User.objects.create_user(username='auser', password='apass')
        self.client.login(username='auser', password='apass')

        resp = self.client.get('/blog/post/the-post', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['num_comments'], 5)

    def test_like_comment(self):
        c = CommentFactory(likes=1)
        u = User.objects.create_user(username='auser', password='apass')
        self.client.login(username='auser', password='apass')

        resp = self.client.post(reverse('like'), {'id': c.pk})
        self.assertEqual('2', resp.content)

        resp = self.client.post(reverse('like'), {'id': c.pk})
        self.assertEqual('1', resp.content)

    def test_archive(self):
        BlogPostFactory.create_batch(20)
        context = print_dates()
        dates = context['archives']

        found_posts = 0
        for date in dates:
            resp = self.client.get(reverse('archive',
                                           kwargs={'archive_slug': date[1]}))
            posts = resp.context['posts']
            self.assertFalse(len(posts) == 0)
            found_posts += len(posts)

        self.assertEqual(20, found_posts)

        resp = self.client.get(reverse('archive',
                                       kwargs={'archive_slug': 'July-2012'}))
        self.assertEqual(len(resp.context['posts']), 0)

        resp = self.client.get(reverse('archive',
                                       kwargs={'archive_slug': 'July'}))
        self.assertContains(resp, "There was an error", 1)

    def test_post_comment(self):
        post = BlogPostFactory()
        slug = post.slug
        user = UserFactory()
        self.client.login(username=user.username, password=user.password)
        comment = "This is a comment"

        resp = self.client.post(reverse('post_comment'),
                                {'post_comment': comment},
                                follow=True)
        self.assertContains(resp, comment, 1)


class TestForms(TestCase):

    def test_userForm(self):
        # test that empty form is rejected
        data = {'username': '', 'password': '', 'email': ''}
        form = userForm(data)
        self.assertFalse(form.is_valid())

        # test that email is optional
        data = {'username': 'auser', 'password': 'apass', 'email': ''}
        form = userForm(data)
        self.assertTrue(form.is_valid())
