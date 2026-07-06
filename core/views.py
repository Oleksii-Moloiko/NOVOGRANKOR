from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import render

from .models import Advantage, Category, Gallery, Monument, SiteSettings


def home(request):
    categories = (
        Category.objects
        .filter(is_active=True)
        .prefetch_related(
            Prefetch(
                "monuments",
                queryset=Monument.objects.filter(is_active=True).order_by("order", "id"),
                to_attr="active_monuments",
            )
        )
        .order_by("order", "id")
    )
    
    advantages = Advantage.objects.filter(
        is_active=True,
    ).order_by("order", "id")

    process_gallery = Gallery.objects.filter(
        section=Gallery.Section.PROCESS,
        is_active=True,
    ).order_by("order", "id")

    works_gallery = Gallery.objects.filter(
        section=Gallery.Section.WORKS,
        is_active=True,
    ).order_by("order", "id")

    site_settings = SiteSettings.objects.first()

    return render(
        request,
        "index.html",
        {
            "categories": categories,
            "advantages": advantages,
            "process_gallery": process_gallery,
            "works_gallery": works_gallery,
            "site_settings": site_settings,
        },
    )


def healthcheck(request):
    return JsonResponse({"status": "ok"})
