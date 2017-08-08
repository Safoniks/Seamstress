from django.db import models


class WorkerOperation(models.Model):
    worker = models.ForeignKey('worker.Worker')
    operation = models.ForeignKey('operation.Operation')
    done = models.PositiveIntegerField(blank=True, default=0)

    def increase_done(self, amount=0):
        self.done += amount
        self.save()

        operation_cost = self.operation.operation_type.full_cost
        self.worker.daily_salary += operation_cost * amount
        self.worker.daily_done += amount
        self.worker.save()


class Worker(models.Model):
    user = models.OneToOneField('user.MyUser')
    brigade = models.ForeignKey('brigade.Brigade', null=True, blank=True, on_delete=models.SET_NULL)
    worker_operations = models.ManyToManyField('operation.Operation', through='worker.WorkerOperation')
    goal = models.FloatField(blank=True, null=True)
    daily_done = models.PositiveIntegerField(blank=True, default=0)
    daily_salary = models.FloatField(blank=True, default=0)
    is_active = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.user.username
