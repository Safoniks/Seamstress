from django.db import models

from public.models import WorkerOperationLogs, WorkerTiming


class WorkerOperation(models.Model):
    worker = models.ForeignKey('worker.Worker')
    operation = models.ForeignKey('operation.Operation')
    done = models.PositiveIntegerField(blank=True, default=0)

    def operation_done(self, amount):
        worker = self.worker
        product = self.operation.product
        operation_type = self.operation.operation_type
        operation_cost = operation_type.full_cost
        done_cost = operation_cost * amount

        self.done += amount
        self.save()

        worker.daily_salary += done_cost
        worker.monthly_salary += done_cost
        worker.daily_done += amount
        worker.save()

        worker_operation_log = WorkerOperationLogs(
            worker=worker,
            operation_type=operation_type,
            product=product,
            done=amount,
            cost=done_cost,
        )
        worker_operation_log.save()


class Worker(models.Model):
    user = models.OneToOneField('user.MyUser')
    brigade = models.ForeignKey('brigade.Brigade', null=True, blank=True, on_delete=models.SET_NULL)
    worker_operations = models.ManyToManyField('operation.Operation', through='worker.WorkerOperation')
    goal = models.FloatField(blank=True, null=True)
    daily_done = models.PositiveIntegerField(blank=True, default=0)
    daily_salary = models.FloatField(blank=True, default=0)
    monthly_salary = models.FloatField(blank=True, default=0)
    is_working = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.user.username

    def get_last_timing(self):
        timing = WorkerTiming.objects.filter(worker=self).last()
        return timing

    def start_working(self):
        worker_timing = WorkerTiming(
            worker=self,
            start=True
        )
        self.is_working = True

        worker_timing.save()
        self.save()

    def stop_working(self):
        worker_timing = WorkerTiming(
            worker=self,
            start=False
        )
        self.is_working = False

        worker_timing.save()
        self.save()
