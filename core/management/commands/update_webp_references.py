from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models import ImageField


class Command(BaseCommand):
    help = "Оновлює посилання в ImageField з JPG/PNG на WEBP"

    def handle(self, *args, **options):
        updated = 0
        missing = 0

        for model in apps.get_models():
            image_fields = [
                field for field in model._meta.get_fields()
                if isinstance(field, ImageField)
            ]

            if not image_fields:
                continue

            self.stdout.write(f"\nМодель: {model.__name__}")

            for obj in model.objects.all():
                changed = False

                for field in image_fields:
                    file = getattr(obj, field.name)

                    if not file:
                        continue

                    old_name = file.name

                    if old_name.lower().endswith(".webp"):
                        continue

                    webp_name = str(Path(old_name).with_suffix(".webp"))

                    try:
                        if file.storage.exists(webp_name):
                            file.name = webp_name
                            changed = True
                            updated += 1

                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"✔ {old_name} -> {webp_name}"
                                )
                            )
                        else:
                            missing += 1
                            self.stdout.write(
                                self.style.WARNING(
                                    f"✘ Не знайдено: {webp_name}"
                                )
                            )

                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f"{old_name}: {e}"
                            )
                        )

                if changed:
                    obj.save()

        self.stdout.write("\n----------------------")
        self.stdout.write(self.style.SUCCESS(f"Оновлено: {updated}"))
        self.stdout.write(self.style.WARNING(f"Не знайдено WebP: {missing}"))
