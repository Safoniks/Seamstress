from datetime import timedelta, datetime, time

from django.utils import timezone
from django.db import models
from django.conf import settings

from utils import get_working_days, get_working_days_amount

from public.models import WorkerOperationLogs, WorkerTiming, Payroll
from simple_history.models import HistoricalRecords


class WorkerOperation(models.Model):
    """
    I am docstring
    """

    worker = models.ForeignKey('worker.Worker')  #: I am reference to worker instance
    operation = models.ForeignKey('operation.Operation')
    history = HistoricalRecords(table_name='worker_operation_history')

    class Meta:
        db_table = 'worker_operation'
        verbose_name = 'worker operation'
        verbose_name_plural = 'worker operations'

    def operation_done(self, amount):
        worker = self.worker
        product = self.operation.product
        operation_type = self.operation.operation_type

        worker_operation_log = WorkerOperationLogs(
            worker=worker,
            operation_type=operation_type,
            product=product,
            done=amount,
        )
        worker_operation_log.save()


class Goal(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    amount = models.FloatField()
    start = models.DateTimeField(blank=True)
    end = models.DateTimeField(blank=True)

    class Meta:
        db_table = 'goal'
        verbose_name = 'goal'
        verbose_name_plural = 'goals'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.start = timezone.now()
        self.end = timezone.now() + timedelta(days=settings.APPLICATION_SETTINGS['salary_days'])
        super(Goal, self).save(*args, **kwargs)

    @property
    def is_active(self):
        return self.end > timezone.now()

    @property
    def tempo(self):
        until = timezone.now()
        return self.worker.get_tempo_in_interval(since=self.start, until=until)

    @property
    def default_salary_timedelta(self):
        working_days = get_working_days_amount(self.start, self.end)
        working_hours = settings.APPLICATION_SETTINGS['working_hours']
        return timedelta(hours=working_days*working_hours)

    @property
    def prediction(self):
        current_day = timezone.now().day
        salary_seconds = self.default_salary_timedelta.total_seconds()
        daily_norm_seconds = timedelta(hours=settings.APPLICATION_SETTINGS['working_hours']).total_seconds()

        working_days = get_working_days(self.start, self.end)
        for day in working_days:
            if day.day <= current_day:
                start_day = timezone.make_aware(datetime.combine(day, time.min))
                end_day = timezone.make_aware(datetime.combine(day, time.max))
                time_worked = self.worker.get_time_worked_in_interval(start_day, end_day, with_pause=True).total_seconds()
                abnormality = time_worked - daily_norm_seconds
                # print('day', day.day)
                # print('start end', start_day, end_day)
                # print('time_worked', time_worked/60/60)
                # print('daily_norm_timedelta', daily_norm_seconds/60/60)
                # print('abnormality', abnormality/60/60)
                if day.day == current_day and abnormality < 0:
                    continue
                salary_seconds += abnormality

        # print('prediction hours', salary_seconds/60/60)
        return round(self.tempo * salary_seconds, 2)


class WorkerManager(models.Manager):
    def all_ordered_by(self, prop='last_reset_done'):
        workers = Worker.objects.all()
        return sorted(workers, key=lambda worker: getattr(worker, prop), reverse=True)


class Worker(models.Model):
    user = models.OneToOneField('user.MyUser')
    goal = models.OneToOneField('worker.Goal', null=True, on_delete=models.SET_NULL)
    brigade = models.ForeignKey('brigade.Brigade', null=True, blank=True, on_delete=models.SET_NULL)
    worker_operations = models.ManyToManyField('operation.Operation', through='worker.WorkerOperation')
    history = HistoricalRecords(table_name='worker_history')

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
        midnight = datetime(current_time.year, current_time.month, current_time.day, tzinfo=timezone.get_current_timezone())
        return {
            'DAILY': {
                'since': midnight,
                'until': current_time,
            },
            'LAST_RESET': {
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
    def is_last_timing_reset(self):
        return self.timings.last().action == WorkerTiming.RESET

    @property
    def last_reset(self):
        last_reset = self.timings.filter(action=WorkerTiming.RESET).last()
        return last_reset.date if last_reset else self.user.date_joined

    @property
    def last_payroll(self):
        last_payroll = self.payrolls.last()
        return last_payroll.date if last_payroll else self.user.date_joined

    @property
    def daily_done_duration(self):
        return self.get_done_in_interval(**self.interval.get('DAILY'), field='duration')

    @property
    def last_reset_time_worked(self):
        return self.get_time_worked_in_interval(**self.interval.get('LAST_RESET'))

    @property
    def last_reset_done(self):
        return self.get_done_in_interval(**self.interval.get('LAST_RESET'))

    @property
    def last_reset_salary(self):
        return self.get_done_in_interval(**self.interval.get('LAST_RESET'), field='cost')

    @property
    def last_period_done(self):
        return self.get_done_in_interval(**self.interval.get('LAST_PERIOD'))

    @property
    def last_period_salary(self):
        return self.get_done_in_interval(**self.interval.get('LAST_PERIOD'), field='cost')

    @property
    def last_period_salary_with_debt(self):
        payrolls = self.payrolls.aggregate(total_paid=models.Sum('paid'))
        debt = self.all_time_salary - (payrolls['total_paid'] or 0)
        return round(debt, 2)

    @property
    def all_time_done(self):
        return self.get_done_in_interval(**self.interval.get('ALL_TIME'))

    @property
    def all_time_salary(self):
        return self.get_done_in_interval(**self.interval.get('ALL_TIME'), field='cost')

    def get_time_worked_in_interval(self, since, until, with_pause=False):
        time_worked = timedelta()
        timings = self.timings.filter(date__gt=since, date__lt=until)

        if timings:
            stop_timings = timings.filter(action=WorkerTiming.STOP)
            start_timings = timings.filter(action=WorkerTiming.START)

            first_timer = timings.first()
            last_timer = timings.last()
            last_is_reset = last_timer.action == WorkerTiming.RESET
            first_is_stop = first_timer.action == WorkerTiming.STOP
            first_is_start = first_timer.action == WorkerTiming.START
            last_is_start = last_timer.action == WorkerTiming.START

            if with_pause:
                if start_timings.exists():
                    time_worked = until - since
                    for start_timing in start_timings:
                        if start_timing.is_prev_reset:
                            if start_timing == first_timer:
                                time_worked -= start_timing.date - since
                            else:
                                time_worked -= start_timing.get_delta(with_reset=True)
                    if last_is_reset:
                        time_worked -= until - last_timer.date
                if not first_is_start:
                    time_worked += first_timer.date - since
                if not last_is_reset:
                    time_worked -= until - timezone.now()
            else:
                if start_timings.exists():
                    if last_is_start:
                        time_worked = until - first_timer.date

                        if first_is_start:
                            start_timings = start_timings[1:]
                        for start_timing in start_timings:
                            time_worked -= start_timing.get_delta()
                    else:
                        if first_is_stop:
                            stop_timings = stop_timings[1:]
                        for stop in stop_timings:
                            time_worked += stop.get_delta()
                if not first_is_start:
                    time_worked += first_timer.date - since
        else:
            last_timing_before = self.timings.filter(date__lt=until).last()
            if last_timing_before and last_timing_before.action == WorkerTiming.START:
                time_worked = until - since

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
        time_worked = self.get_time_worked_in_interval(since=since, until=until, with_pause=True).total_seconds()
        # print('tempo goal hours', time_worked/60/60)
        if time_worked:
            return tempo_field / time_worked
        return 0

    def get_rating_position_with(self, prop='last_reset_done'):
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
