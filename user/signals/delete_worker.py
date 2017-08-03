from django.db.models.signals import post_delete
from django.dispatch import receiver

from worker.models import Worker


@receiver(post_delete, sender=Worker)
def delete_worker(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()
