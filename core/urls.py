from django.urls import path

from .views import home, healthcheck
from django.http import HttpResponse
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from core.sitemaps import StaticViewsSitemap


sitemaps = {

    "static": StaticViewsSitemap,

}

urlpatterns = [
    path("", home, name="home"),
    path("healthcheck/", healthcheck, name="healthcheck"),
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain",
        ),
        name="robots",
    ),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
