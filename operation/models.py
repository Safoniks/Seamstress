from django.db import models


class Operation(models.Model):
    product = models.ForeignKey('product.Product')
    operation_type = models.ForeignKey('operationtype.OperationType')

    def __str__(self):
        return '{product}-{operation_type}'.format(product=self.product.name, operation_type=self.operation_type.name)
