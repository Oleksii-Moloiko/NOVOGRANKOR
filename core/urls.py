from django.urls import path

from .views import home, healthcheck
from django.views.generic import TemplateView


urlpatterns = [
    path("", home, name="home"),
    path("healthcheck/", healthcheck, name="healthcheck"),
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain",
        ),
    ),
]   
