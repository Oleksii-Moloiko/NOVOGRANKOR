import os
from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from django.db.models import ImageField
from PIL import Image, ImageOps


class WebPImageField(ImageField):
    """
    Автоматично:
    - виправляє орієнтацію (EXIF)
    - зменшує фото
    - конвертує у WebP
    """

    def pre_save(self, model_instance, add):
        file = super().pre_save(model_instance, add)

        if not file:

            return file

        # Якщо файл вже WebP

        if file.name.lower().endswith(".webp"):

            return file

        # Якщо файла фізично не існує (наприклад у тестах)

        if not file.storage.exists(file.name):

            return file

        file.seek(0)

        image = Image.open(file)
        image = ImageOps.exif_transpose(image)

        if image.mode != "RGB":
            image = image.convert("RGB")

        image.thumbnail((1920, 1920), Image.Resampling.LANCZOS)

        buffer = BytesIO()

        image.save(
            buffer,
            format="WEBP",
            quality=85,
            optimize=True,
        )

        buffer.seek(0)

        old_path = file.path if hasattr(file, "path") else None

        new_name = Path(file.name).with_suffix(".webp").name

        file.save(
            new_name,
            ContentFile(buffer.read()),
            save=False,
        )

        # Видаляємо оригінальний JPG/PNG
        if (
            old_path
            and os.path.exists(old_path)
            and old_path != file.path
        ):
            try:
                os.remove(old_path)
            except OSError:
                pass

        return file