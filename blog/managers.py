# blog/managers.py

from django.db import models
from django.db.models.query import QuerySet

class EntryMixin(object):
    def live(self):
        return self.get_query_set().filter(status=self.model.STATUS_LIVE)

class EntryQuerySet(QuerySet, EntryMixin):
    pass

class EntryManager(models.Manager, ProjectMixin):
    def get_query_set(self):
        return EntryQuerySet(self.model, using=self._db)