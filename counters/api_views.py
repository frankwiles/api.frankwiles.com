from ninja import ModelSchema
from ninja.security import django_auth

from django.shortcuts import get_object_or_404

from core.api import api
from .models import CounterType
from .service import CounterSummary, counter_summary


@api.get("counters/summary/{slug}", auth=django_auth, response=CounterSummary)
def summary(request, slug: str):
    t = get_object_or_404(CounterType, slug=slug)
    return counter_summary(t)
