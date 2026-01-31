import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Creates a superuser non-interactively if it doesn't exist"

    def handle(self, *args, **options):
        # 1. Get credentials from Environment Variables (The Vault)
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stdout.write("No superuser credentials found in environment. Skipping.")
            return

        # 2. Check if user exists
        if not User.objects.filter(username=username).exists():
            self.stdout.write(f"Creating superuser: {username}")
            # 3. Create the user
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS("Superuser created successfully!"))
        else:
            self.stdout.write("Superuser already exists. Skipping.")