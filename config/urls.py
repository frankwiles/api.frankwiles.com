from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from users.views import UserViewSet, CurrentUserView
from ak.views import (
    HomepageView,
    ForbiddenView,
    InternalServerErrorView,
    NotFoundView,
    OKView,
)

router = routers.SimpleRouter()

router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("", HomepageView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("users/me/", CurrentUserView.as_view(), name="current-user"),
    path("api/v1/", include(router.urls)),
    path("200", OKView.as_view(), name="ok"),
    path("403", ForbiddenView.as_view(), name="forbidden"),
    path("404", NotFoundView.as_view(), name="not_found"),
    path("500", InternalServerErrorView.as_view(), name="internal_server_error"),
    path("health/", include("health_check.urls")),
]
