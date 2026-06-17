from django.db.models import Prefetch
from django.shortcuts import render
from django.http import JsonResponse

from .models import Category, Gallery, Monument


def home(request):
    categories = (
        Category.objects
        .filter(is_active=True)
        .prefetch_related(
            Prefetch(
                "monuments",
                queryset=Monument.objects.filter(
                    is_active=True,
                ).order_by("order", "id"),
            )
        )
        .order_by("order", "id")
    )

    gallery = Gallery.objects.filter(
        is_active=True,
    ).order_by("order", "id")

    return render(
        request,
        "home.html",
        {
            "categories": categories,
            "gallery": gallery,
        },
    )

def healthcheck(request):
    return JsonResponse({"status": "ok"})
