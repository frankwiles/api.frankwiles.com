import json
from django.urls import reverse
from faker import Faker
from counters.models import Counter
from users.models import User


def test_counter_summary(db, tp, lozenge_counter, superuser):
    with tp.login(superuser):
        res = tp.get(
            f"/api/counters/summary/{lozenge_counter.slug}",
            headers={"Accept": "application/json"},
        )
        tp.response_200(res)


def test_create_summary(db, tp, client, lozenge_counter, superuser):
    with tp.login(superuser):
        url = "/api/counters/"
        data = {"type_slug": lozenge_counter.slug, "count": 1}
        print(data)
        res = client.post(url, json.dumps(data), content_type="application/json")
        print(res.status_code)
        print(res.content)
        print(res.json())
        tp.response_200(res)
        assert Counter.objects.filter(type=lozenge_counter).count() == 1
