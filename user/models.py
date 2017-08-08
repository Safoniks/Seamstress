from django.db import models
from django.contrib.auth.models import User


class MyUser(User):
    class Meta:
        proxy = True

    # def is_worker(self):
    #     try:
    #         self.worker
    #         return True
    #     except:
    #         return False
