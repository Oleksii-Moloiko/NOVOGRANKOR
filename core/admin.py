from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Category,
    Monument,
    Gallery,
    ContactRequest,
    SiteSettings,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "order",
    )

    ordering = ("order",)


@admin.register(Monument)
class MonumentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "preview",
        "title",
        "category",
        "order",
    )

    list_filter = (
        "category",
    )

    search_fields = (
        "title",
    )

    ordering = (
        "category",
        "order",
    )

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit:cover;border-radius:8px;" />',
                obj.image.url,
            )
        return "-"

    preview.short_description = "Фото"


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "preview",
    )

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit:cover;border-radius:8px;" />',
                obj.image.url,
            )
        return "-"

    preview.short_description = "Фото"


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "phone",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
    )

    readonly_fields = (
        "name",
        "phone",
        "comment",
        "created_at",
    )

    ordering = (
        "-created_at",
    )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "phone",
        "hero_title",
    )