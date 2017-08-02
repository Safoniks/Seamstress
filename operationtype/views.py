from rest_framework.viewsets import ModelViewSet

from .models import OperationType
from .serializers import (
    OperationTypeSerializer,
)


class OperationTypeViewSet(ModelViewSet):
    queryset = OperationType.objects.all()
    serializer_class = OperationTypeSerializer

