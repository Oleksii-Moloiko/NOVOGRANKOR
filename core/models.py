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
        verbose_name = "Блок «Про компанію»"
        verbose_name_plural = "Блок «Про компанію»"

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
        verbose_name = "Статистика блоку «Про компанію»"
        verbose_name_plural = "Статистика блоку «Про компанію»"
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.value} {self.label}"

class GallerySection(TimeStampedModel):
    class SectionType(models.TextChoices):
        PROCESS = "process", "Процес"
        WORKS = "works", "Наші роботи"

    section_type = models.CharField(
        max_length=20,
        choices=SectionType.choices,
        unique=True,
        verbose_name="Тип секції",
    )

    tag = models.CharField(
        max_length=100,
        verbose_name="Мітка секції",
    )

    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок",
    )

    subtitle = models.TextField(
        blank=True,
        verbose_name="Підзаголовок",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
    )

    class Meta:
        verbose_name = "Заголовок галереї"
        verbose_name_plural = "Заголовки галерей"
        ordering = ["section_type"]

    def __str__(self):
        return f"{self.get_section_type_display()} — {self.title}"
    
class CatalogSection(TimeStampedModel):
    tag = models.CharField(
        max_length=100,
        default="Каталог",
        verbose_name="Мітка секції",
    )

    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок",
    )

    default_price_from = models.PositiveIntegerField(
        default=9000,
        verbose_name="Загальна ціна від",
        help_text="Показується у вкладці 'Всі'. Наприклад: 9000",
    )

    price_hint = models.CharField(
        max_length=255,
        default="Натисніть «Замовити» для уточнення всіх деталей",
        verbose_name="Підказка під ціною",
    )

    price_on_request_text = models.CharField(
        max_length=100,
        default="Ціна уточнюється",
        verbose_name="Текст, якщо ціна не вказана",
    )

    empty_category_text = models.CharField(
        max_length=150,
        default="Товар відсутній",
        verbose_name="Текст порожньої категорії",
    )

    empty_catalog_text = models.CharField(
        max_length=150,
        default="Каталог буде наповнений найближчим часом.",
        verbose_name="Текст порожнього каталогу",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
    )

    class Meta:
        verbose_name = "Блок каталогу"
        verbose_name_plural = "Блок каталогу"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk and CatalogSection.objects.exists():
            return
        super().save(*args, **kwargs)

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
        ordering = ["category__order", "order", "id"]

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
        ordering = ["section", "order", "id"]

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

    brand_subtitle = models.CharField(
        max_length=150,
        default="Збережіть памʼять про найрідніших",
        verbose_name="Підпис біля логотипу",
    )

    hero_eyebrow = models.CharField(
        max_length=150,
        default="● Виготовлення та встановлення по всій Україні",
        verbose_name="Мітка Hero-блоку",
    )

    hero_viber_button_text = models.CharField(
        max_length=100,
        default="Написати в Viber",
        verbose_name="Текст кнопки Viber у Hero",
    )

    cta_primary_button_text = models.CharField(
        max_length=100,
        default="Отримати безкоштовний прорахунок",
        verbose_name="Текст основної CTA-кнопки",
    )

    cta_viber_button_text = models.CharField(
        max_length=100,
        default="Звʼязатися в Viber",
        verbose_name="Текст Viber-кнопки в CTA",
    )

    footer_description = models.TextField(
        default="Виготовлення та встановлення памʼятників з натурального граніту по всій Україні.",
        verbose_name="Опис у футері",
    )

    footer_slogan = models.CharField(
        max_length=150,
        default="Збережіть памʼять про найрідніших",
        verbose_name="Слоган у футері",
    )

    copyright_text = models.CharField(
        max_length=150,
        default="© 2026 NOVOGRANKOR. Усі права захищено.",
        verbose_name="Copyright",
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
    
