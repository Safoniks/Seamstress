from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    RetrieveDestroyAPIView,
)

from operation.models import Operation
from brigade.models import Brigade

from .models import Worker, WorkerOperation
from .serializers import (
    WorkerListSerializer,
    WorkerOperationCreateSerializer,
    WorkerUpdateSerializer,
    CommonOperationSerializer,
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

    def update(self, request, *args, **kwargs):
        data = request.data
        worker = self.worker
        worker_serializer = WorkerUpdateSerializer(worker, data=data)
        if worker_serializer.is_valid():
            worker_serializer.save()
            response_data = WorkerListSerializer(worker).data
            return Response(response_data, status=HTTP_200_OK)
        return Response(worker_serializer.errors, status=HTTP_400_BAD_REQUEST)

    @property
    def worker(self):
        worker_id = self.kwargs.get(self.lookup_url_kwarg)
        worker = get_object_or_404(Worker, id=worker_id)
        return worker


class WorkerOperationCreate(CreateAPIView):
    queryset = WorkerOperation.objects.all()
    serializer_class = WorkerOperationCreateSerializer


class WorkerOperationList(ListAPIView):
    serializer_class = CommonOperationSerializer
    lookup_url_kwarg = 'worker_id'

    def get_queryset(self):
        queryset_list = Operation.objects.filter(worker=self.worker)
        return queryset_list

    @property
    def worker(self):
        worker_id = self.kwargs.get(self.lookup_url_kwarg)
        worker = get_object_or_404(Worker, id=worker_id)
        return worker


class WorkerOperationDetail(RetrieveDestroyAPIView):
    serializer_class = ProductOperationListSerializer
    lookup_url_kwarg = 'operation_id'

    def destroy(self, request, *args, **kwargs):
        worker_id = self.kwargs.get('worker_id')
        operation_id = self.kwargs.get('operation_id')

        worker_operation = get_object_or_404(WorkerOperation, worker=worker_id, operation=operation_id)
        worker_operation.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def get_queryset(self):
        queryset_list = Operation.objects.filter(worker=self.worker)
        return queryset_list

    @property
    def worker(self):
        worker_id = self.kwargs.get(self.lookup_url_kwarg)
        worker = get_object_or_404(Worker, id=worker_id)
        return worker
