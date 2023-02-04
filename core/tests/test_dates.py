from datetime import timedelta
from django.utils import timezone

from core.dates import midnight_today, seven_days_ago, thirty_days_ago


def test_midnight_today():
    now = timezone.now()
    result = midnight_today(now)
    assert result == now.replace(hour=0, minute=0, second=0, microsecond=0)


def test_seven_days_ago():
    now = timezone.now()
    result = seven_days_ago(now)
    assert result.hour == now.hour
    assert result.minute == now.minute
    assert result.second == now.second
    assert result == now - timedelta(days=7)


def test_thirty_days_ago():
    now = timezone.now()
    result = thirty_days_ago(now)
    assert result.hour == now.hour
    assert result.minute == now.minute
    assert result.second == now.second
    assert result == now - timedelta(days=30)
