from datetime import timedelta

from django.db import models
from django.utils import timezone


class CounterTypeQuerySet(models.QuerySet):
    def active(self):
        """Return active CounterTypes"""
        return self.filter(active=True)


class CounterTypeManager(models.Manager):
    def get_queryset(self):
        return CounterTypeQuerySet(self.model, using=self._db)

    def active(self):
        """Return active CounterTypes"""
        return self.get_queryset().filter(active=True)


class CounterQuerySet(models.QuerySet):
    pass


class CounterManager(models.Manager):
    def get_queryset(self):
        return CounterQuerySet(self.model, using=self._db)

    def make_count(self, type_obj, count=1):
        """Create a new count obj"""
        return self.model(type=type_obj, count=count).save()

    def today(self, type_obj):
        now = timezone.now()
