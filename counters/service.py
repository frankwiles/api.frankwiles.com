import datetime
import math

from typing import List

from django.db.models import Avg, Count, Sum
from django.db.models.functions import TruncDay
from django.utils import timezone

from ninja import Schema, ModelSchema
from pydantic import ValidationError, validator

from core.dates import midnight_today, seven_days_ago, thirty_days_ago
from .models import Counter, CounterType


class DayCount(Schema):
    date: datetime.datetime
    count: int


class CounterSummary(Schema):
    """Model for our summary data"""

    today_count: int
    latest_counter: DayCount
    last_7_days_counts: list[DayCount]
    last_7_day_average: int
    last_30_days_counts: list[DayCount]
    last_30_day_average: int


def counter_summary(counter_type):
    """
    Return a summary of information for a given counter type with:

    - Count for today
    - Datetime of last
    - Count for last 7 days
    - Average over last 7 days
    - Count for last 30 days
    - Average over last 30 days
    - Comparison to this time yesterday
    - Comparison to previous 7 day period
    - Comparison to previous 30 day period
    """
    now = timezone.now()
    yesterday = now - datetime.timedelta(days=1)
    this_time_yesterday = now - datetime.timedelta(hours=24)
    midnight = midnight_today(now=now)
    seven_days = seven_days_ago(now=now)
    thirty_days = thirty_days_ago(now=now)

    # Today's count
    today_count = Counter.objects.filter(
        type=counter_type,
        created__gte=midnight,
    ).count()

    # Latest count object
    latest_count = (
        Counter.objects.filter(type=counter_type).order_by("-created").first()
    )

    # Last 7 days counts
    last_7_days = (
        Counter.objects.filter(type=counter_type, created__gte=seven_days)
        .annotate(date=TruncDay("created"))
        .values("date")
        .annotate(count=Sum("count"))
        .order_by("-date")
    )
    last_7_day_average = math.ceil(
        sum([x["count"] for x in last_7_days]) / len(last_7_days)
    )

    # Last 30 days counts
    last_30_days = (
        Counter.objects.filter(type=counter_type, created__gte=thirty_days)
        .annotate(date=TruncDay("created"))
        .values("date")
        .annotate(count=Sum("count"))
        .order_by("-date")
    )
    last_30_day_average = math.ceil(
        sum([x["count"] for x in last_30_days]) / len(last_30_days)
    )

    return {
        "today_count": today_count,
        "latest_counter": {
            "date": latest_count.created,
            "count": latest_count.count,
        },
        "last_7_days_counts": [
            {"date": x["date"], "count": x["count"]} for x in last_7_days
        ],
        "last_7_day_average": last_7_day_average,
        "last_30_days_counts": [
            {"date": x["date"], "count": x["count"]} for x in last_30_days
        ],
        "last_30_day_average": last_30_day_average,
    }


class CounterResponse(ModelSchema):
    """Response schema for counter apis"""

    class Config:
        model = Counter
        model_fields = (
            "id",
            "type",
            "count",
            "created",
            "modified",
        )


class CounterCreate(Schema):
    """Schema for creating a new counter"""

    type_slug: str
    count = 1
