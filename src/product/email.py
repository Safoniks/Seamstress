from copy import deepcopy

from django.conf import settings
from django.core.mail import send_mail

from user.models import MyUser
from product.models import Product


class ProductEmailMessage:
    AVAILABLE_METHODS = ('POST', 'PUT', 'DELETE')

    def __init__(self, request, product):
        if request.method in self.AVAILABLE_METHODS:
            self.request = request
            self.method = request.method
        else:
            raise TypeError(
                'Method {method} is not supported. Available methods: {available_methods}.'.format(
                    method=request.method,
                    available_methods=', '.join(self.AVAILABLE_METHODS)
                )
            )
        if isinstance(product, Product):
            self.product = product
            self.initial_product = deepcopy(product)
            self.initial_product_photos = [photo for photo in product.photos]
            self.initial_product_operations = [operation for operation in product.operations]
        else:
            raise TypeError(
                'Got {type} and you need a {product_class}.'.format(
                    type=type(product),
                    product_class=Product
                )
            )

        self.subject = self._get_subject_templates().get(self.method)
        self.message = self._parse_product()

    @property
    def to_emails(self):
        directors = MyUser.objects.all_directors()
        return [director.email for director in directors]

    @property
    def from_email(self):
        return settings.DEFAULT_FROM_EMAIL

    def _get_subject_templates(self):
        product_name = self.product.name
        return {
            'POST': 'Created new product "%s"' % product_name,
            'PUT': 'Updated product "%s"' % product_name,
            'DELETE': 'Deleted product "%s"' % product_name,
        }

    def _parse_product(self):
        template = '''
{separator}
Name: {product_name}
Description: {product_description}

Photos: {product_photos}

Operations: {product_operations}
{separator}

'''
        product = self.product
        separator = 'PRODUCT'.center(70, '-')
        product_name = product.name
        product_description = product.description

        product_photos = '' if product.photos else None
        for photo in product.photos:
            product_photos += '\n  * {}'.format(self.request.build_absolute_uri(photo.photo.url))

        product_operations = '' if product.operations else None
        for operation in product.operations:
            product_operations += '\n  * {}'.format(operation.operation_type.name)

        return template.format(
            separator=separator,
            product_name=product_name,
            product_description=product_description,
            product_photos=product_photos,
            product_operations=product_operations,
        )

    def add_product_changes(self):
        initial_product = self.initial_product
        updated_product = self.product

        separator = 'CHANGES'.center(70, '-') + '\n'
        changes = separator
        if initial_product.name != updated_product.name:
            changes += 'name: "{old}" CHANGED TO "{new}"\n'.format(
                old=initial_product.name,
                new=updated_product.name
            )
        if initial_product.description != updated_product.description:
            changes += 'description: "{old}" CHANGED TO "{new}"\n'.format(
                old=initial_product.description,
                new=updated_product.description
            )

        initial_photos = self.initial_product_photos
        updated_photos = updated_product.photos
        for photo in initial_photos:
            if photo not in updated_photos:
                changes += 'REMOVED PHOTO {photo}\n'.format(photo=photo.photo.name)
        for photo in updated_photos:
            if photo not in initial_photos:
                changes += 'ADDED NEW PHOTO {photo}\n'.format(photo=self.request.build_absolute_uri(photo.photo.url))

        initial_operations = self.initial_product_operations
        updated_operations = updated_product.operations
        for operation in initial_operations:
            if operation not in updated_operations:
                changes += 'REMOVED OPERATION {operation}\n'.format(operation=operation.operation_type.name)
        for operation in updated_operations:
            if operation not in initial_operations:
                changes += 'ADDED NEW OPERATION {operation}\n'.format(operation=operation.operation_type.name)

        changes += separator
        self.message += changes
        self.message += self._parse_product()

    @property
    def args_mail(self):
        return (
            self.subject,
            self.message,
            self.from_email,
            self.to_emails
        )

    def send_mail(self):
        send_mail(*self.args_mail, fail_silently=True)


'''
Subject: request.method + product

Message:

----PRODUCT------
name: Dress
description: Best

photos:
  * photo.path
  * photo.path

operations:
  * type.name
  * type.name
----PRODUCT----

-----CHANGES-------
name: Dress CHANGED TO Shirt
description: Best CHANGED TO Worst
REMOVED PHOTO photo.path
ADDED NEW PHOTO photo.path
REMOVED OPERATION type.name
ADDED NEW OPERATION type.name
-----CHANGES-----
'''