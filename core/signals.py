from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from core.models import (
    AboutSection,
    Gallery,
    Monument,
)

@receiver(pre_save)
def delete_old_image(sender, instance, **kwargs):
    if sender not in (Monument, Gallery, AboutSection):
        return

    if not instance.pk:
        return

    try:
        old = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    for field in sender._meta.fields:
        if not hasattr(field, "upload_to"):
            continue

        old_file = getattr(old, field.name)
        new_file = getattr(instance, field.name)

        if (
            old_file
            and new_file
            and old_file.name != new_file.name
        ):
            old_file.delete(save=False)


@receiver(post_delete)
def delete_image(sender, instance, **kwargs):
    if sender not in (Monument, Gallery, AboutSection):
        return

    for field in sender._meta.fields:
        if not hasattr(field, "upload_to"):
            continue

        file = getattr(instance, field.name)

        if file:
            file.delete(save=False)