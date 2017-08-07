from django.db import models


class WorkerOperation(models.Model):
    worker = models.ForeignKey('worker.Worker')
    operation = models.ForeignKey('operation.Operation')
    done = models.PositiveIntegerField(blank=True, default=0)


class Worker(models.Model):
    user = models.OneToOneField('user.MyUser')
    brigade = models.ForeignKey('brigade.Brigade', null=True, blank=True, on_delete=models.SET_NULL)
    worker_operations = models.ManyToManyField('operation.Operation', through='worker.WorkerOperation')

    def __str__(self):
        return self.user.username
