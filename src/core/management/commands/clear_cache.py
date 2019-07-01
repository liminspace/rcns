from django.core.cache import cache
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Clear cache.'

    def handle(self, *args, **options):
        print('Clear cache...')
        cache.clear()
        print('Done.')
