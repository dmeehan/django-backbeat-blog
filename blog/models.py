# blog/models.py

import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.db.models import permalink
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

from django_markup.fields import MarkupField
from django_markup.markup import formatter
from taggit.managers import TaggableManager

from blog.managers import PostManager

class TextBlockBase(models.Model):
    """
        An abstract content block with
        title, excerpt, and body fields. Includes behavior to
        allow excerpt and body to be marked up with a variety of tools and
        translated to html.
    """
    title = models.CharField(max_length=100)
    excerpt = models.TextField()
    body = models.TextField()
    markup = MarkupField(default=settings.BLOG_MARKUP_DEFAULT)

    # Fields to store generated HTML. For use with a markup syntax such as Markdown or Textile
    excerpt_html = models.TextField(editable=False, blank=True)
    body_html = models.TextField(editable=False, blank=True)

    def render_markup(self):
        if settings.BLOG_MARKUP_DEFAULT == 'wysiwyg':
            self.markup = "none"
            self.body_html = self.body
            self.excerpt_html = self.excerpt
        else:
            self.body_html = mark_safe(formatter(self.body, filter_name=self.markup))
            self.excerpt_html = mark_safe(formatter(self.excerpt, filter_name=self.markup))


    def save(self, force_insert=False, force_update=False):
        self.render_markup()
        super(TextBlockBase, self).save(force_insert, force_update)

    def __unicode__(self):
        return u'%s' % self.title


    class Meta:
        abstract = True


class StatusMixin(models.Model):
    """
        Allow for a content block to be marked with a status

    """

    STATUS_LIVE = 1
    STATUS_HIDDEN = 2
    STATUS_PENDING = 3
    STATUS_DRAFT = 4
    STATUS_CHOICES = (
        (STATUS_LIVE, 'Live'),
        (STATUS_PENDING, 'Pending'),
        (STATUS_DRAFT, 'Draft'),
        (STATUS_HIDDEN, 'Hidden'),
    )

    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES,
                                              default=STATUS_LIVE,
                                              help_text="Only content with live status will be publicly displayed.")

    class Meta:
        abstract = True


class PostMixin(models.Model):
    """
        A mixin for a posted content type. Adds a published date and the ability to
        find the next and previous post by that date. Adds a slug unique to the
        published date. Adds the ability to associate the post with a user.
    """

    # metadata
    author = models.ForeignKey(User, blank=True, null=True)
    date_published = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        abstract = True


class ArticleBase(TextBlockBase, PostMixin, StatusMixin):
    """
        An abstract blog type article, which combines the fields, behaviors and
        attributes of TextBlockBase, PostMixin, and StatusMixin.

    """
    slug = models.SlugField(unique_for_date='date_published')
    
    class Meta:
        abstract = True

class Post(ArticleBase):
    """
        An article post for the blog. Post is a non-abstract model that
        adds the ability to enable comments and to classify the
        article via tags.
    """
    objects = PostManager()

    enable_comments = models.BooleanField(default=True)
    visits = models.IntegerField(default=0, editable=False) #to keep track of most popular posts

    # taxonomy
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['-date_published']
        get_latest_by = 'date_published'

    def get_previous_post(self):
        return self.get_previous_by_date_published(status=self.STATUS_LIVE)

    def get_next_post(self):
        return self.get_next_by_date_published(status=self.STATUS_LIVE)

    @permalink
    def get_absolute_url(self):
        return ('blog_post_detail', None, {
            'year': self.date_published.year,
            'month': self.date_published.strftime('%b').lower(),
            'day': self.date_published.day,
            'slug': self.slug
        })

class PostImage(models.Model):
    """
        An image associated with a blog post
    """
    image = models.ImageField(upload_to='images/blog')
    post = models.ForeignKey(Post)