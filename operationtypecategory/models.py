from django.db import models


class OperationTypeCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    cost_per_second = models.FloatField()

    class Meta:
        db_table = 'operation_type_category'
        verbose_name = 'operation type category'
        verbose_name_plural = 'operation type categories'

    def __str__(self):
        return self.name
