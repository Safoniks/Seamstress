from django.http import Http404

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveDestroyAPIView,
    CreateAPIView,
)

from operation.models import Operation

from .models import Worker, WorkerOperation
from .serializers import (
    WorkerListSerializer,
    WorkerOperationCreateSerializer,
    WorkerUpdateSerializer,
    CommonOperationSerializer,
    PayrollCreateSerializer,
)

from operation.serializers import ProductOperationListSerializer


class WorkerList(ListAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerListSerializer


class WorkerDetail(RetrieveUpdateDestroyAPIView):
    queryset = Worker.objects.all()
    lookup_url_kwarg = 'worker_id'

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return WorkerUpdateSerializer
        return WorkerListSerializer


class WorkerOperationList(ListCreateAPIView):
    lookup_url_kwarg = 'worker_id'

    def get_queryset(self):
        if not self.worker:
            raise Http404
        queryset_list = Operation.objects.filter(worker=self.worker)
        return queryset_list

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WorkerOperationCreateSerializer
        return CommonOperationSerializer

    @property
    def worker(self):
        worker_id = self.kwargs.get(self.lookup_url_kwarg)
        worker = Worker.objects.filter(id=worker_id).first()
        return worker


class WorkerOperationDetail(RetrieveDestroyAPIView):
    serializer_class = ProductOperationListSerializer
    lookup_url_kwarg = 'operation_id'

    def destroy(self, request, *args, **kwargs):
        worker_id = self.kwargs.get('worker_id')
        operation_id = self.kwargs.get('operation_id')

        worker_operation = WorkerOperation.objects.filter(worker=worker_id, operation=operation_id)
        worker_operation.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def get_queryset(self):
        if not self.worker:
            raise Http404
        queryset_list = Operation.objects.filter(worker=self.worker)
        return queryset_list

    @property
    def worker(self):
        worker_id = self.kwargs.get('worker_id')
        worker = Worker.objects.filter(id=worker_id).first()
        return worker


class PayrollToWorker(CreateAPIView):
    serializer_class = PayrollCreateSerializer
    lookup_url_kwarg = 'worker_id'

    @property
    def worker(self):
        worker_id = self.kwargs.get(self.lookup_url_kwarg)
        worker = Worker.objects.filter(id=worker_id).first()
        return worker
