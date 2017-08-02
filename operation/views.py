import os
import shutil

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveDestroyAPIView,
)

from mixins.mixins import MultipleFieldLookupMixin

from product.models import Product

from .models import Operation
from .serializers import (
    ProductOperationListSerializer,
)


class ProductOperationList(ListCreateAPIView):
    queryset = Operation.objects.all()
    serializer_class = ProductOperationListSerializer

    def perform_create(self, serializer):
        serializer.save(product=self.product)

    @property
    def product(self):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        return product
