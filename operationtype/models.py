from django.db import models


class OperationType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey('operationtypecategory.OperationTypeCategory', on_delete=models.PROTECT)
    duration = models.PositiveIntegerField()

    class Meta:
        db_table = 'operation_type'
        verbose_name = 'operation type'
        verbose_name_plural = 'operation types'

    def __str__(self):
        return self.name

    @property
    def full_cost(self):
        return self.category.cost_per_second * self.duration
