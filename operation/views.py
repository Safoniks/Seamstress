from django.shortcuts import get_object_or_404

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveDestroyAPIView,
)

from product.models import Product

from .models import Operation
from .serializers import (
    ProductOperationListSerializer,
)


class ProductOperationList(ListCreateAPIView):
    serializer_class = ProductOperationListSerializer

    def get_queryset(self):
        queryset_list = Operation.objects.filter(product=self.product)
        return queryset_list

    def perform_create(self, serializer):
        serializer.save(product=self.product)

    @property
    def product(self):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        return product


class ProductOperationDetail(RetrieveDestroyAPIView):
    queryset = Operation.objects.all()
    serializer_class = ProductOperationListSerializer
    lookup_url_kwarg = 'operation_id'


