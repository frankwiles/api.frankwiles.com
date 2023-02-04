from ninja import ModelSchema
from ninja.security import django_auth

from core.api import api
from .models import User


class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "is_active",
            "is_staff",
            "is_superuser",
            "data",
        ]


@api.get("users/me/", auth=django_auth, response=UserSchema)
def me(request):
    return request.user
