from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageOps

from core.models import AboutSection, Gallery, Monument


class Command(BaseCommand):
    help = "Конвертує зображення сайту у WebP і зменшує їхній розмір."

    def add_arguments(self, parser):
        parser.add_argument(
            "--quality",
            type=int,
            default=82,
            help="Якість WebP від 1 до 100. За замовчуванням: 82.",
        )

        parser.add_argument(
            "--max-width",
            type=int,
            default=1400,
            help="Максимальна ширина зображення.",
        )

        parser.add_argument(
            "--max-height",
            type=int,
            default=1400,
            help="Максимальна висота зображення.",
        )

    def handle(self, *args, **options):
        quality = options["quality"]
        max_size = (
            options["max_width"],
            options["max_height"],
        )

        targets = [
            (
                "Monument",
                Monument.objects.exclude(image=""),
                "image",
            ),
            (
                "AboutSection",
                AboutSection.objects.exclude(image=""),
                "image",
            ),
            (
                "Gallery poster",
                Gallery.objects.exclude(poster=""),
                "poster",
            ),
        ]

        processed = 0
        skipped = 0
        failed = 0

        for label, queryset, field_name in targets:
            for instance in queryset.iterator():
                image_field = getattr(
                    instance,
                    field_name,
                    None,
                )

                if not image_field:
                    skipped += 1
                    continue

                try:
                    changed = self.optimize_field(
                        instance=instance,
                        field_name=field_name,
                        quality=quality,
                        max_size=max_size,
                    )

                    if changed:
                        processed += 1

                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Оптимізовано: "
                                f"{label} #{instance.pk}"
                            )
                        )
                    else:
                        skipped += 1

                except Exception as error:
                    failed += 1

                    self.stderr.write(
                        self.style.ERROR(
                            f"Помилка: {label} "
                            f"#{instance.pk}: {error}"
                        )
                    )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Готово. Оптимізовано: {processed}; "
                f"пропущено: {skipped}; "
                f"помилок: {failed}."
            )
        )

    def optimize_field(
        self,
        *,
        instance,
        field_name,
        quality,
        max_size,
    ):
        image_field = getattr(
            instance,
            field_name,
        )

        old_name = image_field.name

        if not old_name:
            return False

        image_field.open("rb")

        try:
            with Image.open(image_field) as source:
                image = ImageOps.exif_transpose(
                    source
                )

                if image.mode not in ("RGB", "RGBA"):
                    if "A" in image.getbands():
                        image = image.convert("RGBA")
                    else:
                        image = image.convert("RGB")

                image.thumbnail(
                    max_size,
                    Image.Resampling.LANCZOS,
                )

                output = BytesIO()

                image.save(
                    output,
                    format="WEBP",
                    quality=quality,
                    method=6,
                    optimize=True,
                )

        finally:
            image_field.close()

        output.seek(0)

        path = Path(old_name)

        new_name = str(
            path.with_suffix(".webp")
        )

        storage = image_field.storage

        if new_name != old_name and storage.exists(
            new_name
        ):
            storage.delete(new_name)

        saved_name = storage.save(
            new_name,
            ContentFile(output.read()),
        )

        setattr(
            instance,
            field_name,
            saved_name,
        )

        instance.save(
            update_fields=[field_name]
        )

        if (
            old_name != saved_name
            and storage.exists(old_name)
        ):
            storage.delete(old_name)

        return True