from datetime import timedelta

from django.utils import timezone
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
    time_worked = models.DurationField(blank=True, default=timedelta())
    last_reset = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    @property
    def brigade_name(self):
        brigade = self.brigade
        if brigade:
            return brigade.name
        return None

    @property
    def timings(self):
        timings = WorkerTiming.objects.filter(worker=self)
        return timings

    def get_last_timing(self):
        return self.timings.last()

    def get_newest_timings(self):
        return self.timings.filter(date__gt=self.last_reset)

    def refresh_time_worked(self):
        time_worked = timedelta()
        timings = self.get_newest_timings()
        stop_timings = timings.filter(start=False)
        start_timings = timings.filter(start=True)
        start_timer = start_timings.first()

        if timings.exists() and start_timer:
            if self.is_working:
                current_time = timezone.now()
                start_timings = start_timings[1:]

                time_worked = current_time - start_timer.date
                if start_timings.exists():
                    for start_timing in start_timings:
                        time_worked -= start_timing.delta

            else:
                if stop_timings.exists():
                    for stop_timing in stop_timings:
                        time_worked += stop_timing.delta

            self.time_worked = time_worked
            self.save()

    def start_stop_timer(self, is_start):
        worker_timing = WorkerTiming(
            worker=self,
            start=is_start
        )
        self.is_working = is_start

        worker_timing.save()
        self.save()

    def reset_timer(self):
        self.time_worked = timedelta()
        self.last_reset = timezone.now()
        self.save()
