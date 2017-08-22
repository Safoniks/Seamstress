from rest_framework.viewsets import ModelViewSet

from user.permissions import IsAuthenticatedDirector

from .models import OperationTypeCategory
from .serializers import (
    OperationTypeCategorySerializer,
)


class OperationTypeCategoryViewSet(ModelViewSet):
    queryset = OperationTypeCategory.objects.all()
    serializer_class = OperationTypeCategorySerializer
    lookup_url_kwarg = 'operation_type_category_id'
    permission_classes = (IsAuthenticatedDirector, )
