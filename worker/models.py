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


class Goal(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    amount = models.FloatField()
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField()

    class Meta:
        db_table = 'goal'
        verbose_name = 'goal'
        verbose_name_plural = 'goals'

    def __str__(self):
        return self.name

    @property
    def is_active(self):
        return self.end > timezone.now()

    @property
    def tempo(self):
        until = timezone.now() if self.is_active else self.end
        return self.worker.get_tempo_in_interval(since=self.start, until=until)


class WorkerManager(models.Manager):
    def all_ordered_by(self, prop='daily_done'):
        workers = Worker.objects.all()
        return sorted(workers, key=lambda worker: getattr(worker, prop), reverse=True)


class Worker(models.Model):
    user = models.OneToOneField('user.MyUser')
    goal = models.OneToOneField('worker.Goal', null=True, on_delete=models.SET_NULL)
    brigade = models.ForeignKey('brigade.Brigade', null=True, blank=True, on_delete=models.SET_NULL)
    worker_operations = models.ManyToManyField('operation.Operation', through='worker.WorkerOperation')

    objects = WorkerManager()

    class Meta:
        db_table = 'worker'
        verbose_name = 'worker'
        verbose_name_plural = 'workers'

    def __str__(self):
        return self.user.username

    @property
    def interval(self):
        current_time = timezone.now()
        return {
            'DAILY': {
                'since': self.last_reset,
                'until': current_time,
            },
            'LAST_PERIOD': {
                'since': self.last_payroll,
                'until': current_time,
            },
            'ALL_TIME': {
                'since': self.user.date_joined,
                'until': current_time,
            },
        }

    @property
    def is_active(self):
        last_timing = self.timings.last()
        return bool(last_timing) and last_timing.action == WorkerTiming.START

    @property
    def brigade_name(self):
        brigade = self.brigade
        if brigade:
            return brigade.name
        return None

    @property
    def operations(self):
        return self.worker_operations.all()

    @property
    def timings(self):
        return WorkerTiming.objects.filter(worker=self)

    @property
    def payrolls(self):
        return Payroll.objects.filter(worker=self)

    @property
    def done_operations(self):
        return WorkerOperationLogs.objects.filter(worker=self)

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
        return self.get_time_worked_in_interval(**self.interval.get('DAILY'))

    @property
    def daily_done(self):
        return self.get_done_in_interval(**self.interval.get('DAILY'))

    @property
    def daily_salary(self):
        return self.get_done_in_interval(**self.interval.get('DAILY'), field='cost')

    @property
    def last_period_done(self):
        return self.get_done_in_interval(**self.interval.get('LAST_PERIOD'))

    @property
    def last_period_salary(self):
        return self.get_done_in_interval(**self.interval.get('LAST_PERIOD'), field='cost')

    @property
    def all_time_done(self):
        return self.get_done_in_interval(**self.interval.get('ALL_TIME'))

    @property
    def all_time_salary(self):
        return self.get_done_in_interval(**self.interval.get('ALL_TIME'), field='cost')

    def get_time_worked_in_interval(self, since, until):
        time_worked = timedelta()
        timings = self.timings.filter(date__gt=since, date__lt=until)
        stop_timings = timings.filter(action=WorkerTiming.STOP)
        start_timings = timings.filter(action=WorkerTiming.START)

        first_timer = timings.first()
        last_timer = timings.last()
        first_is_stop = bool(first_timer) and first_timer.action == WorkerTiming.STOP
        last_is_start = bool(last_timer) and last_timer.action == WorkerTiming.START

        if start_timings.exists():
            if last_is_start:
                time_worked = until - first_timer.date

                if not first_is_stop:
                    start_timings = start_timings[1:]
                for start_timing in start_timings:
                    time_worked -= start_timing.delta
            else:
                if first_is_stop:
                    stop_timings = stop_timings[1:]
                for stop in stop_timings:
                    time_worked += stop.delta
        if first_is_stop:
            time_worked += first_timer.date - since
        return time_worked

    def get_done_in_interval(self, since, until, field='done', operation=None):
        result = 0
        done_operations = self.done_operations.filter(created__gt=since, created__lt=until)
        if operation:
            done_operations = done_operations.filter(operation=operation)
        if done_operations.exists():
            for done_operation in done_operations:
                result += getattr(done_operation, field)
        return round(result, 2)

    def get_tempo_in_interval(self, since, until, field='cost'):
        tempo_field = self.get_done_in_interval(since=since, until=until, field=field)
        time_worked = self.get_time_worked_in_interval(since=since, until=until).seconds
        print('worked', time_worked/60)
        if time_worked:
            return 60 * 60 * tempo_field / time_worked
        return 0

    def get_rating_position_with(self, prop='daily_done'):
        workers = self.__class__.objects.all_ordered_by(prop=prop)
        for i, worker in enumerate(workers):
            if worker == self:
                return i + 1

    def timer_do(self, action):
        worker_timing = WorkerTiming(
            worker=self,
            action=action
        )
        worker_timing.save()
