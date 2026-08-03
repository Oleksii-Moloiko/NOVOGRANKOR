from django.core.paginator import EmptyPage, Paginator
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string

from .models import (
    AboutSection,
    Advantage,
    CatalogSection,
    Category,
    Gallery,
    GallerySection,
    Monument,
    SiteSettings,
)


CATALOG_PAGE_SIZE = 10


def home(request):
    categories = (
        Category.objects
        .filter(is_active=True)
        .order_by("order", "id")
    )

    initial_monuments = (
        Monument.objects
        .filter(
            is_active=True,
            category__is_active=True,
        )
        .select_related("category")
        .order_by(
            "category__order",
            "category_id",
            "order",
            "id",
        )[:CATALOG_PAGE_SIZE]
    )

    total_monuments = Monument.objects.filter(
        is_active=True,
        category__is_active=True,
    ).count()

    about_section = (
        AboutSection.objects.filter(is_active=True)
        .prefetch_related("stats")
        .first()
    )

    process_section = GallerySection.objects.filter(
        section_type=GallerySection.SectionType.PROCESS,
        is_active=True,
    ).first()

    works_section = GallerySection.objects.filter(
        section_type=GallerySection.SectionType.WORKS,
        is_active=True,
    ).first()

    catalog_section = CatalogSection.objects.filter(
        is_active=True,
    ).first()

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
            "initial_monuments": initial_monuments,
            "total_monuments": total_monuments,
            "advantages": advantages,
            "about_section": about_section,
            "catalog_section": catalog_section,
            "process_gallery": process_gallery,
            "works_gallery": works_gallery,
            "process_section": process_section,
            "works_section": works_section,
            "site_settings": site_settings,
        },
    )


def catalog_partial(request):
    category_id = request.GET.get("category", "all")
    page_number = request.GET.get("page", 1)

    monuments = (
        Monument.objects
        .filter(
            is_active=True,
            category__is_active=True,
        )
        .select_related("category")
    )

    category = None

    if category_id != "all":
        category = get_object_or_404(
            Category,
            pk=category_id,
            is_active=True,
        )

        monuments = monuments.filter(
            category=category,
        ).order_by(
            "order",
            "id",
        )
    else:
        monuments = monuments.order_by(
            "category__order",
            "category_id",
            "order",
            "id",
        )

    paginator = Paginator(
        monuments,
        CATALOG_PAGE_SIZE,
    )

    try:
        page_obj = paginator.page(page_number)
    except (EmptyPage, ValueError):
        return JsonResponse(
            {
                "html": "",
                "has_more": False,
                "remaining": 0,
            }
        )

    html = render_to_string(
        "partials/catalog_items.html",
        {
            "page_obj": page_obj,
            "site_settings": SiteSettings.objects.first(),
        },
        request=request,
    )

    loaded_count = page_obj.end_index()

    remaining = max(
        paginator.count - loaded_count,
        0,
    )

    return JsonResponse(
        {
            "html": html,
            "has_more": page_obj.has_next(),
            "remaining": remaining,
        }
    )

def healthcheck(request):
    return JsonResponse({"status": "ok"})