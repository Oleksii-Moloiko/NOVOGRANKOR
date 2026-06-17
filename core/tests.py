from django.contrib.admin.sites import AdminSite
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .admin import CategoryAdmin, GalleryAdmin, MonumentAdmin, SiteSettingsAdmin
from .models import Category, Gallery, Monument, SiteSettings


class CategoryModelTests(TestCase):
    def test_category_str_returns_name(self):
        category = Category.objects.create(
            name="Одинарні памʼятники",
            order=1,
        )

        self.assertEqual(str(category), "Одинарні памʼятники")

    def test_category_default_is_active_true(self):
        category = Category.objects.create(
            name="Подвійні памʼятники",
        )

        self.assertTrue(category.is_active)


class MonumentModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Одинарні памʼятники",
        )

    def test_monument_str_returns_title(self):
        monument = Monument.objects.create(
            category=self.category,
            title="Памʼятник гранітний",
            image="monuments/test.jpg",
        )

        self.assertEqual(str(monument), "Памʼятник гранітний")

    def test_monument_default_is_active_true(self):
        monument = Monument.objects.create(
            category=self.category,
            title="Памʼятник",
            image="monuments/test.jpg",
        )

        self.assertTrue(monument.is_active)


class GalleryModelTests(TestCase):
    def test_gallery_str_returns_title_if_exists(self):
        item = Gallery.objects.create(
            title="Робочий процес",
            video="gallery/videos/test.mp4",
        )

        self.assertEqual(str(item), "Робочий процес")

    def test_gallery_str_returns_default_if_title_empty(self):
        item = Gallery.objects.create(
            video="gallery/videos/test.mp4",
        )

        self.assertEqual(str(item), f"Відео #{item.id}")

    def test_gallery_default_is_active_true(self):
        item = Gallery.objects.create(
            video="gallery/videos/test.mp4",
        )

        self.assertTrue(item.is_active)


class SiteSettingsModelTests(TestCase):
    def test_site_settings_str(self):
        settings = SiteSettings.objects.create(
            phone="+380671234567",
            phone_display="+38 (067) 123-45-67",
            hero_title="Виготовлення памʼятників",
        )

        self.assertEqual(str(settings), "Налаштування сайту")

    def test_only_one_site_settings_instance_allowed(self):
        SiteSettings.objects.create(
            phone="+380671234567",
            phone_display="+38 (067) 123-45-67",
            hero_title="Перші налаштування",
        )

        second_settings = SiteSettings(
            phone="+380931234567",
            phone_display="+38 (093) 123-45-67",
            hero_title="Другі налаштування",
        )

        with self.assertRaises(ValidationError):
            second_settings.full_clean()


class HomeViewTests(TestCase):
    def setUp(self):
        self.active_category = Category.objects.create(
            name="Активна категорія",
            order=1,
            is_active=True,
        )

        self.inactive_category = Category.objects.create(
            name="Неактивна категорія",
            order=2,
            is_active=False,
        )

        self.active_monument = Monument.objects.create(
            category=self.active_category,
            title="Активний памʼятник",
            image="monuments/active.jpg",
            is_active=True,
        )

        self.inactive_monument = Monument.objects.create(
            category=self.active_category,
            title="Неактивний памʼятник",
            image="monuments/inactive.jpg",
            is_active=False,
        )

        self.inactive_category_monument = Monument.objects.create(
            category=self.inactive_category,
            title="Памʼятник у неактивній категорії",
            image="monuments/inactive-category.jpg",
            is_active=True,
        )

        self.active_gallery_item = Gallery.objects.create(
            title="Активне відео",
            video="gallery/videos/active.mp4",
            is_active=True,
        )

        self.inactive_gallery_item = Gallery.objects.create(
            title="Неактивне відео",
            video="gallery/videos/inactive.mp4",
            is_active=False,
        )

        SiteSettings.objects.create(
            phone="+380671234567",
            phone_display="+38 (067) 123-45-67",
            telegram="https://t.me/test",
            viber="https://invite.viber.com/test",
            whatsapp="https://wa.me/380671234567",
            hero_title="Виготовлення памʼятників під ключ",
            hero_subtitle="Збережіть памʼять про найрідніших",
            cta_title="Потрібна консультація?",
            cta_subtitle="Зателефонуйте нам — допоможемо підібрати памʼятник.",
        )

    def test_home_page_returns_200(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse("home"))

        self.assertTemplateUsed(response, "home.html")

    def test_home_page_shows_active_category(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Активна категорія")

    def test_home_page_does_not_show_inactive_category(self):
        response = self.client.get(reverse("home"))

        self.assertNotContains(response, "Неактивна категорія")

    def test_home_page_shows_active_monument(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Активний памʼятник")

    def test_home_page_does_not_show_inactive_monument(self):
        response = self.client.get(reverse("home"))

        self.assertNotContains(response, "Неактивний памʼятник")

    def test_home_page_shows_active_gallery_item(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Активне відео")

    def test_home_page_does_not_show_inactive_gallery_item(self):
        response = self.client.get(reverse("home"))

        self.assertNotContains(response, "Неактивне відео")

    def test_home_page_shows_phone_from_site_settings(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, 'href="tel:+380671234567"')
        self.assertContains(response, "+38 (067) 123-45-67")

    def test_home_page_shows_messenger_links_from_site_settings(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "https://t.me/test")
        self.assertContains(response, "https://invite.viber.com/test")
        self.assertContains(response, "https://wa.me/380671234567")

    def test_home_page_does_not_contain_online_order_form(self):
        response = self.client.get(reverse("home"))

        self.assertNotContains(response, "<form")
        self.assertNotContains(response, "Залишити заявку")
        self.assertNotContains(response, "Надіслати заявку")
        self.assertNotContains(response, "Замовити онлайн")


class AdminSmokeTests(TestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_category_admin_registered_configuration(self):
        admin = CategoryAdmin(Category, self.site)

        self.assertIn("name", admin.search_fields)
        self.assertIn("is_active", admin.list_filter)

    def test_monument_admin_registered_configuration(self):
        admin = MonumentAdmin(Monument, self.site)

        self.assertIn("title", admin.search_fields)
        self.assertIn("category", admin.list_filter)
        self.assertIn("is_active", admin.list_filter)

    def test_gallery_admin_registered_configuration(self):
        admin = GalleryAdmin(Gallery, self.site)

        self.assertIn("title", admin.search_fields)
        self.assertIn("is_active", admin.list_filter)

    def test_site_settings_admin_disallows_add_when_settings_exists(self):
        SiteSettings.objects.create(
            phone="+380671234567",
            phone_display="+38 (067) 123-45-67",
            hero_title="Виготовлення памʼятників",
        )

        admin = SiteSettingsAdmin(SiteSettings, self.site)

        self.assertFalse(admin.has_add_permission(request=None))

class HealthcheckTests(TestCase):
    def test_healthcheck_returns_ok(self):
        response = self.client.get(reverse("healthcheck"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})