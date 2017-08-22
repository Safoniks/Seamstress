from django.db import models


class OperationType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey('operationtypecategory.OperationTypeCategory')
    duration = models.PositiveIntegerField()
    full_cost = models.FloatField(blank=True)

    class Meta:
        db_table = 'operation_type'
        verbose_name = 'operation type'
        verbose_name_plural = 'operation types'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.full_cost = self.category.cost_per_second * self.duration
        super(OperationType, self).save(*args, **kwargs)
