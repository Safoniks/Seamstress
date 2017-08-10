from django.db import models
from django.utils import timezone


class WorkerOperationLogs(models.Model):
    worker = models.ForeignKey('worker.Worker')
    operation_type = models.ForeignKey('operationtype.OperationType', null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey('product.Product', null=True, on_delete=models.SET_NULL)
    done = models.PositiveIntegerField(default=0)
    cost = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)


class WorkerTiming(models.Model):
    worker = models.ForeignKey('worker.Worker')
    start = models.BooleanField()
    delta = models.DurationField(null=True, blank=True)
    date = models.DateTimeField(blank=True)

    class Meta:
        ordering = ['date']

    def save(self, *args, **kwargs):
        current_time = timezone.now()
        self.date = current_time

        last_timing = self.worker.get_last_timing()
        if last_timing:
            prev_time = last_timing.date
            self.delta = current_time - prev_time
        super(WorkerTiming, self).save()
