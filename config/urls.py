from django.urls import include, path, re_path
from django.contrib import admin
from ak.views import (
    FrontendView,
    HomepageView,
    ForbiddenView,
    InternalServerErrorView,
    NotFoundView,
    OKView,
)

import users.api_views
import counters.api_views
from core.api import api

urlpatterns = [
    path("", HomepageView.as_view(), name="home"),
    re_path("^homepage/", FrontendView.as_view(), name="frontend"),
    path("api/", api.urls),
    path("admin/", admin.site.urls),
    path("200", OKView.as_view(), name="ok"),
    path("403", ForbiddenView.as_view(), name="forbidden"),
    path("404", NotFoundView.as_view(), name="not_found"),
    path("500", InternalServerErrorView.as_view(), name="internal_server_error"),
    path("health/", include("health_check.urls")),
]

admin.site.site_header = "api.frankwiles.com"
