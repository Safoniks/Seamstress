import os
import shutil

from django.db import models
from django.conf import settings

from operation.models import Operation
from simple_history.models import HistoricalRecords


def get_image_path(instance, filename):
    return os.path.join(settings.PRODUCT_PHOTOS_DIR_NAME, str(instance.product.id), filename)


class ProductPhotoManager(models.Manager):
    def get_queryset(self):
        return super(ProductPhotoManager, self).get_queryset().filter(active=True)


class ProductPhoto(models.Model):
    product = models.ForeignKey('product.Product', related_name='product_photos')
    photo = models.ImageField(upload_to=get_image_path, null=True, blank=True)
    active = models.BooleanField(blank=True, default=False)
    history = HistoricalRecords(table_name='product_photo_history')

    objects = models.Manager()
    active_objects = ProductPhotoManager()

    class Meta:
        db_table = 'product_photo'
        verbose_name = 'product photo'
        verbose_name_plural = 'product photos'

    @property
    def path(self):
        return os.path.join(settings.MEDIA_ROOT, self.photo.name)

    def activate(self):
        self.active = True
        self.save()

    def delete(self, *args, **kwargs):
        ret = super(ProductPhoto, self).delete(*args, **kwargs)
        try:
            os.remove(self.path)
        except OSError:
            pass
        return ret


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    operations = models.ManyToManyField('operationtype.OperationType', through='operation.Operation')
    history = HistoricalRecords(table_name='product_history')

    class Meta:
        db_table = 'product'
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name

    @property
    def photos(self):
        return ProductPhoto.active_objects.filter(product=self)

    @property
    def all_photos(self):
        return ProductPhoto.objects.filter(product=self)

    @property
    def operations(self):
        return Operation.objects.filter(product=self)

    @property
    def path_photos(self):
        return os.path.join(settings.MEDIA_ROOT, settings.PRODUCT_PHOTOS_DIR_NAME, str(self.id))

    def delete(self, *args, **kwargs):
        path_photos = self.path_photos
        ret = super(Product, self).delete(*args, **kwargs)
        try:
            shutil.rmtree(path_photos)
        except OSError:
            pass
        return ret
