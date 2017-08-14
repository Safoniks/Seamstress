from django.db import models


class Brigade(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'brigade'
        verbose_name = 'brigade'
        verbose_name_plural = 'brigades'

    def __str__(self):
        return self.name
