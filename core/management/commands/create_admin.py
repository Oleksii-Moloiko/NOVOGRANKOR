import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create default admin user if it does not exist."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not email or not password:
            self.stdout.write(
                self.style.WARNING(
                    "Admin user was not created because DJANGO_SUPERUSER_* variables are missing."
                )
            )
            return

        User = get_user_model()

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.SUCCESS(f"Admin user '{username}' already exists.")
            )
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write(
            self.style.SUCCESS(f"Admin user '{username}' was created.")
        )