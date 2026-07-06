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

class Advantage(TimeStampedModel):
    class Icon(models.TextChoices):
        LOCATION = "location", "Локація"
        CUBE = "cube", "3D-візуалізація"
        DELIVERY = "delivery", "Доставка"

    title = models.CharField(
        max_length=100,
        verbose_name="Заголовок",
    )

    description = models.TextField(
        verbose_name="Опис",
    )

    icon = models.CharField(
        max_length=30,
        choices=Icon.choices,
        default=Icon.LOCATION,
        verbose_name="Іконка",
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
        verbose_name = "Перевага"
        verbose_name_plural = "Переваги"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

class AboutSection(TimeStampedModel):
    tag = models.CharField(
        max_length=100,
        default="Про компанію",
        verbose_name="Мітка секції",
    )

    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок",
    )

    text_1 = models.TextField(
        verbose_name="Перший абзац",
    )

    text_2 = models.TextField(
        blank=True,
        verbose_name="Другий абзац",
    )

    text_3 = models.TextField(
        blank=True,
        verbose_name="Третій абзац",
    )

    card_kicker = models.CharField(
        max_length=150,
        verbose_name="Мітка картки",
    )

    card_title = models.CharField(
        max_length=255,
        verbose_name="Заголовок картки",
    )

    card_description = models.TextField(
        verbose_name="Опис картки",
    )

    image = models.ImageField(
        upload_to="about/",
        blank=True,
        verbose_name="Зображення",
        help_text="Наприклад, карта України або інше зображення для лівої картки.",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
    )

    class Meta:
        verbose_name = "Блок про компанію"
        verbose_name_plural = "Блок про компанію"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk and AboutSection.objects.exists():
            return
        super().save(*args, **kwargs)


class AboutStat(TimeStampedModel):
    about_section = models.ForeignKey(
        AboutSection,
        on_delete=models.CASCADE,
        related_name="stats",
        verbose_name="Блок про компанію",
    )

    value = models.CharField(
        max_length=50,
        verbose_name="Значення",
        help_text="Наприклад: 10+, 500+",
    )

    label = models.CharField(
        max_length=150,
        verbose_name="Підпис",
        help_text="Наприклад: років досвіду",
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
        verbose_name = "Статистика про компанію"
        verbose_name_plural = "Статистика про компанію"
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.value} {self.label}"

class Category(TimeStampedModel):
    name = models.CharField(
        max_length=100,
        verbose_name="Назва",
    )

    price_from = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Ціна від, грн",
        help_text="Стартова ціна для всієї категорії. Наприклад: 18000",
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

    def get_price_display(self):
        if self.price_from:
            return f"від {self.price_from:,}".replace(",", " ") + " грн"
        return ""

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

    class Section(models.TextChoices):
        PROCESS = "process", "Процес"
        WORKS = "works", "Наші роботи"

    section = models.CharField(
        max_length=20,
        choices=Section.choices,
        default=Section.PROCESS,
        verbose_name="Секція",
    )
    
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

    viber = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="Viber",
        help_text="Повне посилання на Viber.",
    )

    whatsapp = models.URLField(
        blank=True,
        verbose_name="WhatsApp",
        help_text="Повне посилання, наприклад: https://wa.me/380671234567",
    )

    instagram = models.URLField(
        blank=True,
        verbose_name="Instagram",
        help_text="Повне посилання на Instagram.",
    )

    facebook = models.URLField(
        blank=True,
        verbose_name="Facebook",
        help_text="Повне посилання на Facebook.",
    )

    tiktok = models.URLField(
        blank=True,
        verbose_name="TikTok",
        help_text="Повне посилання на TikTok.",
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
    
