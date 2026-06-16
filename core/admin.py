from django.contrib import admin
from .models import (
    Category,
    Monument,
    Gallery,
    ContactRequest
)

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(Monument)
class MonumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "category",
    )

    list_filter = ("category",)

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("id",)

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "phone",
        "created_at",
    )
    readonly_fields = (
        "name",
        "phone",
        "comment",
        "created_at",
    )