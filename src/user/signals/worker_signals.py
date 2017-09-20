from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from worker.models import Worker
from user.models import MyUser


@receiver(post_save, sender=MyUser)
def create_worker(sender, instance, created, **kwargs):
    if created and instance.is_worker():
        new_worker = Worker(user=instance)
        new_worker.save()


@receiver(post_delete, sender=Worker)
def delete_worker(sender, instance, **kwargs):
    if hasattr(instance, 'user'):
        instance.user.delete()
