# blog/urls.py

from django.conf import settings
from django.conf.urls.defaults import *

from blog.models import Entry

urlpatterns = patterns('',
    url(r'^$', EntryIndexView.as_view(), name = 'blog_entry_index'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        DateDetailView.as_view(),
        queryset=Entry._default_manager.live(),
        date_field="date_published",
        name = 'blog_entry_detail'),

    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/$',
        DayArchiveView.as_view(),
        queryset=Entry._default_manager.live(),
        date_field="date_published",
        name='blog_archive_day'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        MonthArchiveView.as_view(),
        queryset=Entry._default_manager.live(),
        date_field="date_published",
        name='blog_archive_month'
    ),
    url(r'^(?P<year>\d{4})/$',
        YearArchiveView.as_view(),
        queryset=Entry._default_manager.live(),
        date_field="date_published",
        name='blog_archive_year'
    ),
    url(r'^categories/(?P<slug>[-\w]+)/$',
        view='category_detail',
        name='blog_category_detail'
    ),
    url (r'^categories/$',
        view='category_list',
        name='blog_category_list'
    ),
    url(r'^tags/(?P<slug>[-\w]+)/$',
        view='tag_detail',
        name='blog_tag_detail'
    ),
    url(r'^page/(?P<page>\d+)/$',
        view='post_list',
        name='blog_index_paginated'
    ),
    url(r'^$',
        view='post_list',
        name='blog_index'
    ),
)
