import os
from django.db import models


def get_image_path(instance, filename):
    # product_dir = '{id}-{name}'.format(id=instance.product.id, name=instance.product.name)
    return os.path.join('product-photos', str(instance.product.id), filename)


class ProductPhoto(models.Model):
    product = models.ForeignKey('Product', related_name='product_photos')
    photo = models.ImageField(upload_to=get_image_path, null=True, blank=True)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name

    @property
    def photos(self):
        return ProductPhoto.objects.filter(product=self)




