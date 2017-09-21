from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView,
)

from product.models import Product

from worker.models import Worker, WorkerOperation
from worker.serializers import WorkerProfileSerializer

from .models import Operation
from .serializers import (
    ProductOperationListSerializer,
)


class ProductOperationList(ListCreateAPIView):
    serializer_class = ProductOperationListSerializer

    def get_queryset(self):
        queryset_list = Operation.objects.filter(product=self.product)
        return queryset_list

    def get_serializer_context(self):
        return {'product': self.product}

    def perform_create(self, serializer):
        serializer.save(product=self.product)

    @property
    def product(self):
        product_id = self.kwargs.get('product_id')
        product = Product.objects.filter(id=product_id).first()
        return product


class ProductOperationDetail(RetrieveDestroyAPIView):
    queryset = Operation.objects.all()
    serializer_class = ProductOperationListSerializer
    lookup_url_kwarg = 'operation_id'


class OperationWorkerList(ListAPIView):
    serializer_class = WorkerProfileSerializer
    lookup_url_kwarg = 'operation_id'

    def get_queryset(self):
        queryset_list = Worker.objects.filter(workeroperation__operation=self.operation)
        return queryset_list

    @property
    def operation(self):
        operation_id = self.kwargs.get(self.lookup_url_kwarg)
        operation = Operation.objects.filter(id=operation_id).first()
        return operation


class OperationWorkerDetail(RetrieveDestroyAPIView):
    serializer_class = WorkerProfileSerializer
    lookup_url_kwarg = 'worker_id'

    def get_queryset(self):
        queryset_list = Worker.objects.filter(workeroperation__operation=self.operation)
        return queryset_list

    def destroy(self, request, *args, **kwargs):
        worker_id = self.kwargs.get('worker_id')
        operation_id = self.kwargs.get('operation_id')

        worker_operation = WorkerOperation.objects.filter(worker=worker_id, operation=operation_id).first()
        worker_operation.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @property
    def operation(self):
        operation_id = self.kwargs.get('operation_id')
        operation = Operation.objects.filter(id=operation_id).first()
        return operation


