from django.db import models


class OperationType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    duration = models.PositiveIntegerField()
    cost_per_second = models.FloatField()
    full_cost = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.full_cost = self.cost_per_second * self.duration
        super(OperationType, self).save(*args, **kwargs)
