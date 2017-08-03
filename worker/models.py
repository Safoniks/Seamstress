from django.db import models


class Worker(models.Model):
    user = models.OneToOneField('user.MyUser')




