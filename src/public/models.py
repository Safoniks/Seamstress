from datetime import timedelta
from django.utils import timezone

from django.db import models


class WorkerOperationLogs(models.Model):
    worker = models.ForeignKey('worker.Worker')
    operation_type = models.ForeignKey('operationtype.OperationType', null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey('product.Product', null=True, on_delete=models.SET_NULL)
    done = models.PositiveIntegerField(default=0)
    cost = models.FloatField(blank=True)
    duration = models.PositiveIntegerField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'worker_operation_logs'
        verbose_name = 'worker operation log'
        verbose_name_plural = 'worker operation logs'

    def save(self, *args, **kwargs):
        self.cost = self.operation_type.full_cost * self.done
        self.duration = self.operation_type.duration * self.done
        super(WorkerOperationLogs, self).save(*args, **kwargs)


class WorkerTiming(models.Model):
    worker = models.ForeignKey('worker.Worker')
    start_date = models.DateTimeField()
    stop_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'worker_timing'
        verbose_name = 'worker timing'
        verbose_name_plural = 'worker timings'

    @property
    def delta(self):
        if not self.stop_date:
            return timezone.now() - self.start_date
        return self.stop_date - self.start_date


class Payroll(models.Model):
    worker = models.ForeignKey('worker.Worker')
    paid = models.FloatField()
    salary = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payroll'
        verbose_name = 'payroll'
        verbose_name_plural = 'payrolls'
        ordering = ['date']

    @property
    def debt(self):
        return self.salary - self.paid
