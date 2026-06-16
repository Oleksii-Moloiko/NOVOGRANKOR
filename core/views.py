from django.shortcuts import render

from .models import Category, SiteSettings


def home(request):
    categories = Category.objects.prefetch_related(
        "monuments"
    )

    site_settings = SiteSettings.objects.first()

    return render(
        request,
        "home.html",
        {
            "categories": categories,
            "site_settings": site_settings,
        }
    )