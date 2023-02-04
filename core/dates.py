from datetime import timedelta

from django.utils import timezone


def midnight_today(now=None):
    """Return the midnight of today"""
    if now is None:
        now = timezone.now()
    return now.replace(hour=0, minute=0, second=0, microsecond=0)


def seven_days_ago(now=None):
    if now is None:
        now = timezone.now()
    return now - timedelta(days=7)


def thirty_days_ago(now=None):
    if now is None:
        now = timezone.now()
    return now - timedelta(days=30)
