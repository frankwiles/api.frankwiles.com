from django.urls import reverse
from faker import Faker
from users.models import User


def test_user_me(db, tp):
    u = User.objects.create(email="test@example.com")
    u.set_password("password")
    u.save()
    with tp.login(u):
        res = tp.get("/api/user/me/", headers={"Accept": "application/json"})
        tp.response_200(res)
