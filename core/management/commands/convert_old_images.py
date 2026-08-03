from pathlib import Path

from django.core.management.base import BaseCommand

from core.models import Monument   # <-- заміни на свою модель


class Command(BaseCommand):
    help = "Оновлює старі JPG/PNG записи до WebP"

    def handle(self, *args, **options):
        updated = 0

        for obj in Monument.objects.all():
            if not obj.image:
                continue

            old_name = obj.image.name

            if old_name.lower().endswith(".webp"):
                continue

            webp_name = str(Path(old_name).with_suffix(".webp"))

            webp_path = Path(obj.image.storage.path(webp_name))

            if not webp_path.exists():
                self.stdout.write(
                    self.style.WARNING(f"WebP не знайдено: {webp_name}")
                )
                continue

            obj.image.name = webp_name
            obj.save(update_fields=["image"])

            updated += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"{old_name} -> {webp_name}"
                )
            )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(f"Оновлено {updated} записів.")
        )
