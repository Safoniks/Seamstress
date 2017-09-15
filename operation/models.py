from django.db import models

from simple_history.models import HistoricalRecords


class Operation(models.Model):
    product = models.ForeignKey('product.Product')
    operation_type = models.ForeignKey('operationtype.OperationType', on_delete=models.PROTECT)
    history = HistoricalRecords(table_name='operation_history')

    class Meta:
        db_table = 'operation'
        verbose_name = 'operation'
        verbose_name_plural = 'operations'

    def __str__(self):
        return '{product}-{operation_type}'.format(product=self.product.name, operation_type=self.operation_type.name)
