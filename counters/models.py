from django.db import models
from django.utils.text import slugify
from django_extensions.db.models import TimeStampedModel

from .managers import CounterTypeManager, CounterManager


class CounterType(TimeStampedModel):
    """
    The type of thing we're counting
    """

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, db_index=True)
    active = models.BooleanField(default=True, db_index=True)

    objects = CounterTypeManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save()


class Counter(TimeStampedModel):
    """
    The type of thing we're counting
    """

    type = models.ForeignKey(CounterType, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    objects = CounterManager()

    def __str__(self):
        return f"{self.type.name}: {self.count}"
