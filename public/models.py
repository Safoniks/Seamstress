from datetime import timedelta

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
    START = 'start'
    STOP = 'stop'
    RESET = 'reset'

    ACTION_CHOICES = (
        (START, START),
        (STOP, STOP),
        (RESET, RESET),
    )

    worker = models.ForeignKey('worker.Worker')
    action = models.CharField(max_length=5, choices=ACTION_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'worker_timing'
        verbose_name = 'worker timing'
        verbose_name_plural = 'worker timings'
        ordering = ['date']

    def get_next(self, queryset):
        next = queryset.filter(date__gt=self.date)
        if next:
            return next.first()
        return False

    def get_prev(self, queryset):
        prev = queryset.filter(date__lt=self.date).order_by('-date')
        if prev:
            return prev.first()
        return False

    def get_delta(self, with_reset=False):
        current_time = self.date
        worker_timings = self.worker.timings
        try:
            prev_timing = self
            while True:
                prev_timing = prev_timing.get_prev(queryset=worker_timings)
                if with_reset or prev_timing.action != self.RESET:
                    break
        except:
            prev_timing = None
        return current_time - prev_timing.date if prev_timing else timedelta()

    @property
    def is_prev_reset(self):
        worker_timings = self.worker.timings
        try:
            prev_timing = self.get_prev(queryset=worker_timings).action
        except AttributeError:
            return True
        return prev_timing == self.RESET


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
