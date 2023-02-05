import pytest

from users.models import User


@pytest.fixture
def user(db):
    user = User.objects.create(
        email="user@example.com", first_name="John", last_name="Doe"
    )
    user.set_password("password")
    user.save()
    return user


@pytest.fixture
def superuser(db):
    user = User.objects.create(
        email="admin@example.com",
        first_name="John",
        last_name="Admin",
        is_superuser=True,
        is_staff=True,
    )
    user.set_password("password")
    user.save()
    return user
