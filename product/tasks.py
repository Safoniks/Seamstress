import logging
import os

from django.core.mail import send_mail
from django.conf import settings
from seamstress.celery import app

from utils import remove_empty_sub_dirs

from product.models import ProductPhoto


@app.task(bind=True, default_retry_delay=60, max_retries=5, ignore_result=True)
def send_product_mail(self, *args):
    try:
        send_mail(*args, fail_silently=False)
    except Exception as exc:
        raise self.retry(exc=exc)
        # logging.warning('Fail.')


@app.task
def clear_photos():
    photos_dir_path = os.path.join(settings.MEDIA_ROOT, settings.PRODUCT_PHOTOS_DIR_NAME)
    inactive_photos = ProductPhoto.objects.filter(active=False)
    count = 0

    for photo in inactive_photos:
        photo_path = os.path.join(settings.MEDIA_ROOT, photo.photo.name)
        try:
            photo.delete()
        except OSError:
            logging.warning('Photo "%s" does not exist.' % photo_path)
            continue

        count += 1
        logging.info('Successfully removed photo "%s"' % photo_path)

    remove_empty_sub_dirs(photos_dir_path)
    logging.info('Removed photos: %d' % count)



