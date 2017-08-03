from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from worker.models import Worker


@receiver(post_save, sender=User)
def create_worker(sender, instance, created, **kwargs):
    if created and not instance.is_superuser and not instance.is_staff:
        new_worker = Worker(user=instance)
        new_worker.save()
