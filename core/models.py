from django.core.exceptions import ValidationError
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата створення",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата оновлення",
    )

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(
        max_length=100,
        verbose_name="Назва",
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
    )

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class Monument(TimeStampedModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="monuments",
        verbose_name="Категорія",
    )

    title = models.CharField(
        max_length=255,
        verbose_name="Назва",
    )

    image = models.ImageField(
        upload_to="monuments/",
        verbose_name="Фото",
    )

    alt_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Alt-текст для фото",
        help_text="Короткий опис зображення для SEO та доступності.",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Опис",
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активний",
    )

    class Meta:
        verbose_name = "Пам'ятник"
        verbose_name_plural = "Пам'ятники"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Gallery(TimeStampedModel):
    title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Назва відео",
    )

    video = models.FileField(
        upload_to="gallery/videos/",
        blank=True,
        verbose_name="Відео",
        help_text="Рекомендований формат: MP4.",
    )

    poster = models.ImageField(
        upload_to="gallery/posters/",
        blank=True,
        null=True,
        verbose_name="Обкладинка відео",
        help_text="Необовʼязково. Показується як превʼю до запуску відео.",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Опис",
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активне",
    )

    class Meta:
        verbose_name = "Відео галереї"
        verbose_name_plural = "Відео галерея"
        ordering = ["order", "id"]

    def __str__(self):
        if self.title:
            return self.title
        return f"Відео #{self.id}"
class SiteSettings(models.Model):
    phone = models.CharField(
        max_length=30,
        verbose_name="Телефон для посилання",
        help_text="Формат для tel:, наприклад: +380671234567",
    )

    phone_display = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Телефон для відображення",
        help_text="Формат для сайту, наприклад: +38 (067) 123-45-67",
    )

    telegram = models.URLField(
        blank=True,
        verbose_name="Telegram",
        help_text="Повне посилання, наприклад: https://t.me/username",
    )

    viber = models.URLField(
        blank=True,
        verbose_name="Viber",
        help_text="Повне посилання на Viber.",
    )

    whatsapp = models.URLField(
        blank=True,
        verbose_name="WhatsApp",
        help_text="Повне посилання, наприклад: https://wa.me/380671234567",
    )

    logo = models.ImageField(
        upload_to="logo/",
        blank=True,
        null=True,
        verbose_name="Логотип",
    )

    hero_title = models.CharField(
        max_length=255,
        verbose_name="Заголовок першого екрану",
    )

    hero_subtitle = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Підзаголовок першого екрану",
    )

    cta_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="CTA заголовок",
        help_text="Наприклад: Потрібна консультація?",
    )

    cta_subtitle = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="CTA підзаголовок",
        help_text="Наприклад: Зателефонуйте нам — допоможемо підібрати памʼятник.",
    )

    instagram = models.URLField(
        blank=True,
        verbose_name="Instagram",
    )

    facebook = models.URLField(
        blank=True,
        verbose_name="Facebook",
    )

    seo_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="SEO Title",
    )

    seo_description = models.TextField(
        blank=True,
        verbose_name="SEO Description",
    )
    class Meta:
        verbose_name = "Налаштування сайту"
        verbose_name_plural = "Налаштування сайту"

    def clean(self):
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError("Можна створити лише один обʼєкт налаштувань сайту.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Налаштування сайту"