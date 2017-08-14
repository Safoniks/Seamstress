from datetime import timedelta

from django.utils import timezone
from django.db import models

from public.models import WorkerOperationLogs, WorkerTiming, Payroll


class WorkerOperation(models.Model):
    worker = models.ForeignKey('worker.Worker')
    operation = models.ForeignKey('operation.Operation')

    class Meta:
        db_table = 'worker_operation'
        verbose_name = 'worker operation'
        verbose_name_plural = 'worker operations'

    def operation_done(self, amount):
        worker = self.worker
        product = self.operation.product
        operation = self.operation
        done_cost = operation.operation_type.full_cost * amount

        worker_operation_log = WorkerOperationLogs(
            worker=worker,
            operation=operation,
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
    is_working = models.BooleanField(blank=True, default=False)

    class Meta:
        db_table = 'worker'
        verbose_name = 'worker'
        verbose_name_plural = 'workers'

    def __str__(self):
        return self.user.username

    @property
    def brigade_name(self):
        brigade = self.brigade
        if brigade:
            return brigade.name
        return None

    @property
    def operations(self):
        operations = self.worker_operations.all()
        return operations

    @property
    def timings(self):
        timings = WorkerTiming.objects.filter(worker=self)
        return timings

    @property
    def payrolls(self):
        payrolls = Payroll.objects.filter(worker=self)
        return payrolls

    @property
    def done_operations(self):
        done_operations = WorkerOperationLogs.objects.filter(worker=self)
        return done_operations

    @property
    def last_reset(self):
        last_reset = self.timings.filter(action=WorkerTiming.RESET).last()
        return last_reset.date if last_reset else self.user.date_joined

    @property
    def last_payroll(self):
        last_payroll = self.payrolls.last()
        return last_payroll.date if last_payroll else self.user.date_joined

    @property
    def daily_time_worked(self):
        since = self.last_reset
        until = timezone.now()
        return self.get_time_worked_in_period(since=since, until=until)

    def get_daily_done(self, field='done', operation=None):
        since = self.last_reset
        until = timezone.now()
        return self.get_done_in_period(since=since, until=until, field=field, operation=operation)

    def get_period_done(self, field='done', operation=None):
        since = self.last_payroll
        until = timezone.now()
        return self.get_done_in_period(since=since, until=until, field=field, operation=operation)

    def get_all_done(self, field='done', operation=None):
        since = self.user.date_joined
        until = timezone.now()
        return self.get_done_in_period(since=since, until=until, field=field, operation=operation)

    def get_time_worked_in_period(self, since, until):
        time_worked = timedelta()
        timings = self.timings.filter(date__gt=since, date__lt=until)
        stop_timings = timings.filter(action=WorkerTiming.STOP)
        start_timings = timings.filter(action=WorkerTiming.START)
        start_timer = start_timings.first()

        if timings.exists() and start_timer:
            if timings.last().action == WorkerTiming.START:
                start_timings = start_timings[1:]

                time_worked = until - start_timer.date
                if start_timings.exists():
                    for start_timing in start_timings:
                        time_worked -= start_timing.delta
            else:
                if stop_timings.exists():
                    for stop in stop_timings:
                        time_worked += stop.delta
        return time_worked

    def get_done_in_period(self, since, until, field='done', operation=None):
        result = 0
        done_operations = self.done_operations.filter(created__gt=since, created__lt=until)
        if operation:
            done_operations = done_operations.filter(operation=operation)
        if done_operations.exists():
            for done_operation in done_operations:
                result += getattr(done_operation, field)
        return round(result, 2)

    def start_timer(self):
        worker_timing = WorkerTiming(
            worker=self,
            action=WorkerTiming.START
        )
        self.is_working = True

        worker_timing.save()
        self.save()

    def stop_timer(self):
        worker_timing = WorkerTiming(
            worker=self,
            action=WorkerTiming.STOP
        )
        self.is_working = False

        worker_timing.save()
        self.save()

    def reset_timer(self):
        worker_timing = WorkerTiming(
            worker=self,
            action=WorkerTiming.RESET
        )
        worker_timing.save()
