from django.db import models

from simple_history.models import HistoricalRecords


class Brigade(models.Model):
    name = models.CharField(max_length=100, unique=True)
    history = HistoricalRecords(table_name='brigade_history')

    class Meta:
        db_table = 'brigade'
        verbose_name = 'brigade'
        verbose_name_plural = 'brigades'

    def __str__(self):
        return self.name
