# blog/views.py

from django.views.generic import DateDetailView, ArchiveIndexView, YearArchiveView, \
    MonthArchiveView, WeekArchiveView, DayArchiveView, TodayArchiveView, \
    DetailView, ListView

from blog.models import *

class EntryDateMixin():
    queryset = Entry._default_manager.live()
    date_field="date_published"

class EntryDetailView(DateDetailView):
    queryset = Entry._default_manager.live()
    date_field="date_published"

class EntryIndexView(ArchiveIndexView):
    queryset = Entry._default_manager.live()

