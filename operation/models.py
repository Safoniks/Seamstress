from django.db import models


class Operation(models.Model):
    product = models.ForeignKey('product.Product')
    operation_type = models.ForeignKey('operationtype.OperationType')
