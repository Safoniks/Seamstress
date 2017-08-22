from django.db.models.signals import post_save
from django.dispatch import receiver

from operationtypecategory.models import OperationTypeCategory
from operationtype.models import OperationType


@receiver(post_save, sender=OperationTypeCategory)
def create_worker(sender, instance, created, **kwargs):
    if not created:
        category = instance
        operation_types = OperationType.objects.filter(category=category)
        for operation_type in operation_types:
            operation_type.save()
