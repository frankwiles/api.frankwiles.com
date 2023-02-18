from ninja import ModelSchema
from ninja.security import django_auth

from django.shortcuts import get_object_or_404

from core.api import api
from .models import CounterType, Counter
from .service import CounterSummary, counter_summary, CounterResponse, CounterCreate


@api.get("counters/summary/{slug}", auth=django_auth, response=CounterSummary)
def summary(request, slug: str):
    t = get_object_or_404(CounterType, slug=slug)
    return counter_summary(t)


@api.post("counters/", auth=django_auth, response=CounterResponse)
def create_counter(request, item: CounterCreate):
    t = get_object_or_404(CounterType, slug=item.type_slug)
    c = Counter.objects.make_count(type_obj=t, count=item.count)

    return c
