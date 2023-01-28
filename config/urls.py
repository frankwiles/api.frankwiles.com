from django.urls import include, path
from django.contrib import admin
from ak.views import (
    HomepageView,
    ForbiddenView,
    InternalServerErrorView,
    NotFoundView,
    OKView,
)

from users.api_views import api

urlpatterns = [
    path("", HomepageView.as_view(), name="home"),
    path("api/", api.urls),
    path("admin/", admin.site.urls),
    path("200", OKView.as_view(), name="ok"),
    path("403", ForbiddenView.as_view(), name="forbidden"),
    path("404", NotFoundView.as_view(), name="not_found"),
    path("500", InternalServerErrorView.as_view(), name="internal_server_error"),
    path("health/", include("health_check.urls")),
]
