import os
from django.db import models
from django.conf import settings


def get_image_path(instance, filename):
    return os.path.join(settings.PRODUCT_PHOTOS_DIR_NAME, str(instance.product.id), filename)


class ProductPhoto(models.Model):
    product = models.ForeignKey('product.Product', related_name='product_photos')
    photo = models.ImageField(upload_to=get_image_path, null=True, blank=True)

    class Meta:
        db_table = 'product_photo'
        verbose_name = 'product photo'
        verbose_name_plural = 'product photos'


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    operations = models.ManyToManyField('operationtype.OperationType', through='operation.Operation')

    class Meta:
        db_table = 'product'
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name

    @property
    def photos(self):
        return ProductPhoto.objects.filter(product=self)
