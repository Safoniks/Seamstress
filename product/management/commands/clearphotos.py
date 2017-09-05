import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from utils import remove_empty_sub_dirs

from product.models import ProductPhoto


class Command(BaseCommand):
    help = 'Removes inactive product photos.'

    def handle(self, *args, **options):
        photos_dir_path = os.path.join(settings.MEDIA_ROOT, settings.PRODUCT_PHOTOS_DIR_NAME)
        inactive_photos = ProductPhoto.objects.filter(active=False)
        count = 0

        for photo in inactive_photos:
            photo_path = os.path.join(settings.MEDIA_ROOT, photo.photo.name)
            try:
                photo.delete()
            except OSError:
                self.stdout.write(self.style.NOTICE('Photo "%s" does not exist.' % photo_path))
                continue

            count += 1
            self.stdout.write(self.style.SUCCESS('Successfully removed photo "%s"' % photo_path))

        remove_empty_sub_dirs(photos_dir_path)
        self.stdout.write(self.style.SUCCESS('Removed photos: %d' % count))
