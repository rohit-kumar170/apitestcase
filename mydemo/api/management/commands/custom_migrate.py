from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

class Command(BaseCommand):
    help = 'Run migrations for all databases defined in settings.DATABASES'

    def handle(self, *args, **options):
        databases = settings.DATABASES.keys()

        for db in databases:
            self.stdout.write(f"Starting migration for database: {db}")
            try:
                call_command('migrate', database=db)
                self.stdout.write(self.style.SUCCESS(f"Successfully migrated {db}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error migrating {db}: {e}"))
