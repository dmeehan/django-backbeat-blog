# blog/models.py

import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink
from django.utils.html import strip_tags

from blocks.models import ArticleBase

from taggit.managers import TaggableManager

class Entry(ArticleBase):
    """
        An article entry for the blog
    """
    enable_comments = models.BooleanField(default=True)

    # taxonomy
    tags = TaggableManager(blank=True)
    categories = models.ManyToManyField(Category, blank=True)

    @permalink
    def get_absolute_url(self):
        return ('blog_entry_detail', None, {
            'year': self.date_published.year,
            'month': self.date_published.strftime('%b').lower(),
            'day': self.date_published.day,
            'slug': self.slug
        })

class EntryImage(models.Model):
    """
        An image associated with a blog entry
    """
    image = models.ImageField()
    entry = models.ForeignKey(Entry)