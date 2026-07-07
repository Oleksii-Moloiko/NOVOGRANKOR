from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Advantage,
    AboutSection,
    AboutStat,
    CatalogSection,
    Category,
    Gallery,
    GallerySection,
    Monument,
    SiteSettings,
)

class TimestampReadonlyMixin:
    readonly_fields = (
        "created_at",
        "updated_at",
    )
class MonumentInline(admin.TabularInline):
    model = Monument
    extra = 0
    fields = (
        "title",
        "image",
        "order",
        "is_active",
    )

    ordering = (
        "order",
        "id",
    )

@admin.register(Advantage)
class AdvantageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "icon",
        "order",
        "is_active",
        "updated_at",
    )

    list_filter = (
        "icon",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
    )

    list_editable = (
        "order",
        "is_active",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "order",
        "id",
    )

    fieldsets = (
        (
            "Основна інформація",
            {
                "fields": (
                    "title",
                    "description",
                    "icon",
                    "is_active",
                )
            },
        ),
        (
            "Сортування",
            {
                "fields": (
                    "order",
                )
            },
        ),
        (
            "Системна інформація",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

class AboutStatInline(admin.TabularInline):
    model = AboutStat
    extra = 0

    fields = (
        "value",
        "label",
        "order",
        "is_active",
    )

    ordering = (
        "order",
        "id",
    )

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "tag",
        "is_active",
        "updated_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "tag",
        "title",
        "text_1",
        "text_2",
        "text_3",
        "card_title",
        "card_description",
    )

    readonly_fields = (
        "image_preview",
        "created_at",
        "updated_at",
    )

    inlines = (
        AboutStatInline,
    )

    fieldsets = (
        (
            "Основний текст",
            {
                "fields": (
                    "tag",
                    "title",
                    "text_1",
                    "text_2",
                    "text_3",
                    "is_active",
                )
            },
        ),
        (
            "Ліва картка",
            {
                "fields": (
                    "card_kicker",
                    "card_title",
                    "card_description",
                    "image",
                    "image_preview",
                )
            },
        ),
        (
            "Системна інформація",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 220px; border-radius: 12px;" />',
                obj.image.url,
            )
        return "-"

    image_preview.short_description = "Превʼю зображення"

    def has_add_permission(self, request):
        if AboutSection.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(GallerySection)
class GallerySectionAdmin(admin.ModelAdmin):
    list_display = (
        "section_type",
        "tag",
        "title",
        "is_active",
        "updated_at",
    )

    list_filter = (
        "section_type",
        "is_active",
    )

    search_fields = (
        "tag",
        "title",
        "subtitle",
    )

    list_editable = (
        "is_active",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Основна інформація",
            {
                "fields": (
                    "section_type",
                    "tag",
                    "title",
                    "subtitle",
                    "is_active",
                )
            },
        ),
        (
            "Системна інформація",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price_from",
        "order",
        "is_active",
        "updated_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )

    list_editable = (
        "price_from",
        "order",
        "is_active",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "order",
        "id",
    )

    fieldsets = (
        (
            "Основна інформація",
            {
                "fields": (
                    "name",
                    "price_from",
                    "is_active",
                )
            },
        ),
        (
            "Сортування",
            {
                "fields": (
                    "order",
                )
            },
        ),
    )

    inlines = (
        MonumentInline,
    )

@admin.register(CatalogSection)
class CatalogSectionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "tag",
        "default_price_from",
        "is_active",
        "updated_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "tag",
        "title",
        "price_hint",
        "price_on_request_text",
        "empty_category_text",
        "empty_catalog_text",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Заголовок секції",
            {
                "fields": (
                    "tag",
                    "title",
                    "is_active",
                )
            },
        ),
        (
            "Ціни та підказки",
            {
                "fields": (
                    "default_price_from",
                    "price_hint",
                    "price_on_request_text",
                )
            },
        ),
        (
            "Порожні стани",
            {
                "fields": (
                    "empty_category_text",
                    "empty_catalog_text",
                )
            },
        ),
        (
            "Системна інформація",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def has_add_permission(self, request):
        if CatalogSection.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(Monument)
class MonumentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "order",
        "is_active",
        "image_preview",
        "updated_at",
    )

    list_filter = (
        "category",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
        "alt_text",
    )

    list_editable = (
        "order",
        "is_active",
    )

    readonly_fields = (
        "image_preview",
        "created_at",
        "updated_at",
    )


    ordering = (
        "category",
        "order",
        "id",
    )

    fieldsets = (
        (
            "Основна інформація",
            {
                "fields": (
                    "category",
                    "title",
                    "alt_text",
                    "is_active",
                )
            },
        ),
        (
            "Зображення",
            {
                "fields": (
                    "image",
                    "image_preview",
                )
            },
        ),
        (
            "Сортування",
            {
                "fields": (
                    "order",
                )
            },
        ),
        (
            "Системна інформація",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 140px; height: auto; border-radius: 10px;" />',
                obj.image.url,
            )
        return "-"

    image_preview.short_description = "Превʼю"

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit:cover;border-radius:8px;" />',
                obj.image.url,
            )
        return "-"

    def price_display(self, obj):
        if obj.category:
            return obj.category.get_price_display()
        return "-"

    preview.short_description = "Фото"
    price_display.short_description = "Ціна"

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "section",
        "order",
        "is_active",
        "video_preview",
        "updated_at",
    )

    list_filter = (
        "section",
        "is_active",
    )

    search_fields = (
        "title",
    )

    list_editable = (
        "order",
        "is_active",
    )

    ordering = (
        "section",
        "order",
        "id",
    )

    readonly_fields = (
        "video_preview",
        "poster_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Відео",
            {
                "fields": (
                    "title",
                    "section",
                    "video",
                    "poster",
                    "description",
                    "is_active",
                )
            },
        ),
        (
            "Сортування",
            {
                "fields": (
                    "order",
                )
            },
        ),
        (
            "Системна інформація",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def poster_preview(self, obj):
        if obj.poster:
            return format_html(
                '<img src="{}" style="max-width: 180px; height: auto; border-radius: 10px;" />',
                obj.poster.url,
            )
        return "-"

    poster_preview.short_description = "Превʼю постера"

    def video_preview(self, obj):
        if obj.video:
            return format_html(
                '<video width="220" controls style="border-radius:8px;">'
                '<source src="{}" type="video/mp4">'
                "Ваш браузер не підтримує відео."
                "</video>",
                obj.video.url,
            )
        return "-"

    video_preview.short_description = "Превʼю відео"
    
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "phone_display",
        "hero_title",
    )

    fieldsets = (
        (
            "Контакти",
            {
                "fields": (
                    "phone",
                    "phone_display",
                    "telegram",
                    "viber",
                    "whatsapp",
                    "instagram",
                    "facebook",
                    "tiktok",
                    "brand_subtitle",
                )
            },
        ),
        (
            "Перший екран",
            {
                "fields": (
                    "logo",
                    "hero_title",
                    "hero_subtitle",
                    "hero_eyebrow",
                    "hero_viber_button_text",
                )
            },
        ),
        (
            "CTA-блок",
            {
                "fields": (
                    "cta_title",
                    "cta_subtitle",
                    "cta_primary_button_text",
                    "cta_viber_button_text",
                )
            },
        ),

        (
            "Футер",
            {
                "fields": (
                    "footer_description",
                    "footer_slogan",
                    "copyright_text",
                )
            },
        ),

        (
            "SEO",
            {
                "fields": (
                    "seo_title",
                    "seo_description",
                )
            },
        ),
    )

    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)