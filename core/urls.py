from django.urls import path

from .views import home, healthcheck
from django.http import HttpResponse

urlpatterns = [
    path("", home, name="home"),
    path("healthcheck/", healthcheck, name="healthcheck"),

    path(
        "robots.txt",
        lambda request: HttpResponse(
            "User-agent: *\nAllow: /",
            content_type="text/plain",
        ),
        name="robots",
    ),
]
