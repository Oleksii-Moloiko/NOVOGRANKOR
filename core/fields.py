import os
from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from django.db.models import ImageField
from PIL import Image, ImageOps


class WebPImageField(ImageField):
    """
    Продакшен ImageField.

    Можливості:
    - автоматичний поворот (EXIF);
    - підтримка прозорості PNG;
    - зменшення великих фото;
    - конвертація у WebP;
    - автоматичне видалення оригінального JPG/PNG.
    """

    def __init__(
        self,
        *args,
        quality=85,
        max_size=(1920, 1920),
        **kwargs,
    ):
        self.quality = quality
        self.max_size = max_size
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        file = super().pre_save(model_instance, add)

        if not file:
            return file

        # якщо файл ще не записаний
        if not file.storage.exists(file.name):
            return file

        file.seek(0)

        image = Image.open(file)
        image = ImageOps.exif_transpose(image)

        # RGB або RGBA (щоб PNG не втрачав прозорість)
        if image.mode not in ("RGB", "RGBA"):
            if "A" in image.getbands():
                image = image.convert("RGBA")
            else:
                image = image.convert("RGB")

        image.thumbnail(
            self.max_size,
            Image.Resampling.LANCZOS,
        )

        buffer = BytesIO()

        image.save(
            buffer,
            format="WEBP",
            quality=self.quality,
            optimize=True,
            method=6,
        )

        buffer.seek(0)

        old_path = file.path if hasattr(file, "path") else None

        directory = Path(file.name).parent
        filename = Path(file.name).stem + ".webp"
        new_name = str(directory / filename)

        file.save(
            new_name,
            ContentFile(buffer.read()),
            save=False,
        )

        # Видаляємо старий jpg/png
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