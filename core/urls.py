from django.urls import path

from .views import home, healthcheck

urlpatterns = [
    path("", home, name="home"),
    path("healthcheck/", healthcheck, name="healthcheck"),
]