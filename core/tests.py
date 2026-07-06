from django.contrib.admin.sites import AdminSite
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .admin import (
    AboutSectionAdmin,
    AdvantageAdmin,
    CatalogSectionAdmin,
    CategoryAdmin,
    GalleryAdmin,
    GallerySectionAdmin,
    MonumentAdmin,
    SiteSettingsAdmin,
)

from .models import (
    AboutSection,
    AboutStat,
    Advantage,
    CatalogSection,
    Category,
    Gallery,
    GallerySection,
    Monument,
    SiteSettings,
)

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

class CatalogSectionModelTests(TestCase):
    def test_catalog_section_str_returns_title(self):
        section = CatalogSection.objects.create(
            tag="Каталог",
            title="Оберіть категорію пам'ятника",
        )

        self.assertEqual(str(section), "Оберіть категорію пам'ятника")

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

class GallerySectionModelTests(TestCase):
    def test_gallery_section_str_returns_type_and_title(self):
        section = GallerySection.objects.create(
            section_type=GallerySection.SectionType.PROCESS,
            tag="Процес",
            title="Від каменю до готового пам'ятника",
            subtitle="Тестовий опис.",
        )

        self.assertEqual(
            str(section),
            "Процес — Від каменю до готового пам'ятника",
        )

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

class AdvantageModelTests(TestCase):
    def test_advantage_str_returns_title(self):
        advantage = Advantage.objects.create(
            title="По всій Україні",
            description="Виготовлення та встановлення памʼятників під ключ.",
            icon=Advantage.Icon.LOCATION,
        )

        self.assertEqual(str(advantage), "По всій Україні")

    def test_advantage_default_is_active_true(self):
        advantage = Advantage.objects.create(
            title="Доставка",
            description="Привозимо готовий виріб на вашу локацію.",
            icon=Advantage.Icon.DELIVERY,
        )

        self.assertTrue(advantage.is_active)


class AboutSectionModelTests(TestCase):
    def test_about_section_str_returns_title(self):
        about = AboutSection.objects.create(
            tag="Про компанію",
            title="Українське виробництво",
            text_1="Перший текст.",
            card_kicker="Працюємо по всій Україні",
            card_title="Доставка у вашому регіоні",
            card_description="Опис картки.",
        )

        self.assertEqual(str(about), "Українське виробництво")


class AboutStatModelTests(TestCase):
    def test_about_stat_str_returns_value_and_label(self):
        about = AboutSection.objects.create(
            tag="Про компанію",
            title="Українське виробництво",
            text_1="Перший текст.",
            card_kicker="Працюємо по всій Україні",
            card_title="Доставка у вашому регіоні",
            card_description="Опис картки.",
        )

        stat = AboutStat.objects.create(
            about_section=about,
            value="10+",
            label="років досвіду",
        )

        self.assertEqual(str(stat), "10+ років досвіду")
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

        self.active_advantage = Advantage.objects.create(
            title="Активна перевага",
            description="Ця перевага має відображатися на сайті.",
            icon=Advantage.Icon.LOCATION,
            order=1,
            is_active=True,
        )

        self.inactive_advantage = Advantage.objects.create(
            title="Неактивна перевага",
            description="Ця перевага не має відображатися на сайті.",
            icon=Advantage.Icon.DELIVERY,
            order=2,
            is_active=False,
        )

        self.about_section = AboutSection.objects.create(
            tag="Про компанію",
            title="Тестовий блок про компанію",
            text_1="Перший тестовий абзац про компанію.",
            text_2="Другий тестовий абзац про компанію.",
            text_3="Третій тестовий абзац про компанію.",
            card_kicker="Працюємо по всій Україні",
            card_title="Тестова доставка у вашому регіоні",
            card_description="Тестовий опис лівої картки.",
            is_active=True,
        )

        self.active_about_stat = AboutStat.objects.create(
            about_section=self.about_section,
            value="10+",
            label="років досвіду",
            order=1,
            is_active=True,
        )
        self.catalog_section = CatalogSection.objects.create(
            tag="Тестовий каталог",
            title="Тестовий заголовок каталогу",
            default_price_from=12000,
            price_hint="Тестова підказка під ціною.",
            price_on_request_text="Тестова ціна уточнюється",
            empty_category_text="Тестова категорія порожня",
            empty_catalog_text="Тестовий каталог порожній",
            is_active=True,
        )

        self.inactive_about_stat = AboutStat.objects.create(
            about_section=self.about_section,
            value="999+",
            label="неактивна статистика",
            order=2,
            is_active=False,
        )

        self.process_section = GallerySection.objects.create(
            section_type=GallerySection.SectionType.PROCESS,
            tag="Тестовий процес",
            title="Тестовий заголовок процесу",
            subtitle="Тестовий підзаголовок процесу.",
            is_active=True,
        )

        self.works_section = GallerySection.objects.create(
            section_type=GallerySection.SectionType.WORKS,
            tag="Тестові роботи",
            title="Тестовий заголовок робіт",
            subtitle="Тестовий підзаголовок робіт.",
            is_active=True,
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
            brand_subtitle="Тестовий підпис бренду",
            hero_eyebrow="Тестова мітка hero",
            hero_viber_button_text="Тестова кнопка Viber hero",
            cta_primary_button_text="Тестова основна CTA кнопка",
            cta_viber_button_text="Тестова CTA Viber кнопка",
            footer_description="Тестовий опис футера.",
            footer_slogan="Тестовий слоган футера",
            copyright_text="© 2026 Тестовий copyright",
        )

    def test_home_page_returns_200(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse("home"))

        self.assertTemplateUsed(response, "index.html")

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

    def test_home_page_shows_catalog_section_heading(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Тестовий каталог")
        self.assertContains(response, "Тестовий заголовок каталогу")

    def test_home_page_shows_catalog_price_hint(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "12000")
        self.assertContains(response, "Тестова підказка під ціною.")

    def test_home_page_shows_phone_from_site_settings(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, 'href="tel:+380671234567"')
        self.assertContains(response, "+38 (067) 123-45-67")

    def test_home_page_shows_brand_subtitle_from_site_settings(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Тестовий підпис бренду")

    def test_home_page_shows_hero_eyebrow_from_site_settings(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Тестова мітка hero")

    def test_home_page_shows_cta_button_texts_from_site_settings(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Тестова основна CTA кнопка")
        self.assertContains(response, "Тестова CTA Viber кнопка")

    def test_home_page_shows_footer_texts_from_site_settings(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Тестовий опис футера.")
        self.assertContains(response, "Тестовий слоган футера")
        self.assertContains(response, "© 2026 Тестовий copyright")

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

    def test_home_page_shows_active_advantage(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Активна перевага")

    def test_home_page_does_not_show_inactive_advantage(self):
        response = self.client.get(reverse("home"))

        self.assertNotContains(response, "Неактивна перевага")

    def test_home_page_shows_about_section(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Тестовий блок про компанію")
        self.assertContains(response, "Перший тестовий абзац про компанію.")
        self.assertContains(response, "Тестова доставка у вашому регіоні")

    def test_home_page_shows_active_about_stat(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "10+")
        self.assertContains(response, "років досвіду")

    def test_home_page_does_not_show_inactive_about_stat(self):
        response = self.client.get(reverse("home"))

        self.assertNotContains(response, "999+")
        self.assertNotContains(response, "неактивна статистика")

    def test_home_page_shows_process_gallery_section_heading(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Тестовий процес")
        self.assertContains(response, "Тестовий заголовок процесу")
        self.assertContains(response, "Тестовий підзаголовок процесу.")

    def test_home_page_shows_works_gallery_section_heading(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Тестові роботи")
        self.assertContains(response, "Тестовий заголовок робіт")
        self.assertContains(response, "Тестовий підзаголовок робіт.")

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

    def test_advantage_admin_registered_configuration(self):
        admin = AdvantageAdmin(Advantage, self.site)

        self.assertIn("title", admin.search_fields)
        self.assertIn("is_active", admin.list_filter)
        self.assertIn("icon", admin.list_filter)

    def test_catalog_section_admin_registered_configuration(self):
        admin = CatalogSectionAdmin(CatalogSection, self.site)

        self.assertIn("title", admin.search_fields)
        self.assertIn("is_active", admin.list_filter)
        self.assertIn("created_at", admin.readonly_fields)

    def test_gallery_section_admin_registered_configuration(self):
        admin = GallerySectionAdmin(GallerySection, self.site)

        self.assertIn("title", admin.search_fields)
        self.assertIn("section_type", admin.list_filter)
        self.assertIn("is_active", admin.list_filter)

    def test_site_settings_admin_disallows_add_when_settings_exists(self):
        SiteSettings.objects.create(
            phone="+380671234567",
            phone_display="+38 (067) 123-45-67",
            hero_title="Виготовлення памʼятників",
        )

        admin = SiteSettingsAdmin(SiteSettings, self.site)

        self.assertFalse(admin.has_add_permission(request=None))

    def test_about_section_admin_registered_configuration(self):
        admin = AboutSectionAdmin(AboutSection, self.site)

        self.assertIn("title", admin.search_fields)
        self.assertIn("is_active", admin.list_filter)
        self.assertIn("image_preview", admin.readonly_fields)

class HealthcheckTests(TestCase):
    def test_healthcheck_returns_ok(self):
        response = self.client.get(reverse("healthcheck"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})