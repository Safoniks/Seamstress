from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

from worker.models import Worker


@receiver(post_save, sender=User)
def create_worker(sender, instance, created, **kwargs):
    if created and not instance.is_superuser and not instance.is_staff:
        new_worker = Worker(user=instance)
        new_worker.save()


@receiver(post_delete, sender=Worker)
def delete_worker(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()