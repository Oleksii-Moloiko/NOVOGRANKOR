from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Назва"
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок"
    )

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ["order"]

    def __str__(self):
        return self.name
    
class Monument(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="monuments",
    )

    title = models.CharField(
        max_length=255,
        verbose_name="Назва"
    )

    image = models.ImageField(
        upload_to="monuments/",
    )

    description = models.TextField(
        blank=True,
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок"
    )

    class Meta:
        verbose_name = "Пам'ятник"
        verbose_name_plural = "Пам'ятники"
        ordering = ["order"]

    def __str__(self):
        return self.title
    
class Gallery(models.Model):
    image = models.ImageField(
        upload_to="gallery/"
    )

    class Meta:
        verbose_name = "Фото галереї"
        verbose_name_plural = "Галерея"

class ContactRequest(models.Model):
    name = models.CharField(max_length=255)

    phone = models.CharField(max_length=50)

    comment = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"{self.name} - {self.phone}"
    
class SiteSettings(models.Model):

    phone = models.CharField(
        max_length=30,
        verbose_name="Телефон"
    )

    telegram = models.URLField(
        blank=True
    )

    whatsapp = models.URLField(
        blank=True
    )

    logo = models.ImageField(
    upload_to="logo/",
    blank=True,
    null=True,
    )

    hero_title = models.CharField(
        max_length=255
    )

    hero_subtitle = models.CharField(
        max_length=255
    )

    class Meta:
        verbose_name = "Налаштування сайту"
        verbose_name_plural = "Налаштування сайту"

    def __str__(self):
        return "Налаштування сайту"