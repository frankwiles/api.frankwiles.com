from ninja import NinjaAPI, ModelSchema
from ninja.security import django_auth

from .models import User

api = NinjaAPI(csrf=True)


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


@api.get("user/me/", auth=django_auth, response=UserSchema)
def me(request):
    return request.user
