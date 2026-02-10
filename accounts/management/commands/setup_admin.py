from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.conf import settings


class Command(BaseCommand):
    help = "Create or Update a superuser using credentials from Django settings"

    def handle(self, *args, **options):
        User = get_user_model()

        email = settings.ADMIN_EMAIL
        password = settings.ADMIN_PASSWORD

        if not email or not password:
            self.stdout.write(
                self.style.ERROR("ADMIN_EMAIL or ADMIN_PASSWORD not found in settings")
            )
            return

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email.split("@")[0],
                "is_active": True,
            },
        )

        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Successfully CREATED admin: {email}")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully PROMOTED/UPDATED existing user to admin: {email}"
                )
            )

        # Update the site domain for emails
        site, site_created = Site.objects.get_or_create(
            id=settings.SITE_ID,
            defaults={
                "domain": "k5tb26hid6.execute-api.us-east-1.amazonaws.com",
                "name": "YoshiBlog",
            },
        )
        if not site_created:
            site.domain = "k5tb26hid6.execute-api.us-east-1.amazonaws.com"
            site.name = "YoshiBlog"
            site.save()
            self.stdout.write(self.style.SUCCESS("Updated site domain for emails"))
