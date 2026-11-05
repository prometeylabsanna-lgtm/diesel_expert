from django.core.management.base import BaseCommand

from landing.seed import seed_if_empty


class Command(BaseCommand):
    help = "Заповнює порожні секції тимчасовим контентом із макета."

    def handle(self, *args, **options):
        seed_if_empty()
        self.stdout.write(self.style.SUCCESS("Контент на місці."))
