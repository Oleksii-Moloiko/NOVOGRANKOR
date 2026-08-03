from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Delete old JPG/JPEG/PNG files if a matching WebP exists."

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT)

        deleted = 0

        for path in media_root.rglob("*"):
            if path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                continue

            webp = path.with_suffix(".webp")

            if webp.exists():
                path.unlink()
                deleted += 1
                self.stdout.write(f"Deleted: {path.relative_to(media_root)}")

        self.stdout.write(
            self.style.SUCCESS(f"\nDone. Deleted {deleted} file(s).")
        )