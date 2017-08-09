from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    GenericAPIView,
)

from operation.models import Operation
from worker.models import WorkerOperation, Worker

from .serializers import (
    PublicOperationListSerializer,
    PublicOperationDoneSerializer,
    PublicWorkerDetailSerializer,
    PublicWorkerUpdateSerializer,
)
from .permissions import IsAuthenticatedWorker


class PublicOperationList(ListAPIView):
    serializer_class = PublicOperationListSerializer
    permission_classes = [IsAuthenticatedWorker]

    def get_queryset(self):
        queryset_list = Operation.objects.filter(worker=self.worker)
        return queryset_list

    @property
    def worker(self):
        return self.request.user.worker


class PublicOperationDetail(RetrieveAPIView):
    serializer_class = PublicOperationListSerializer
    permission_classes = [IsAuthenticatedWorker]
    lookup_url_kwarg = 'operation_id'

    def get_object(self):
        operation_id = self.kwargs.get(self.lookup_url_kwarg)
        operation_obj = Operation.objects.get(worker=self.worker, id=operation_id)
        return operation_obj

    @property
    def worker(self):
        return self.request.user.worker


class PublicOperationDone(CreateAPIView):
    serializer_class = PublicOperationDoneSerializer
    permission_classes = [IsAuthenticatedWorker]
    lookup_url_kwarg = 'operation_id'

    def get_object(self):
        operation_id = self.kwargs.get(self.lookup_url_kwarg)
        operation_obj = Operation.objects.get(worker=self.worker, id=operation_id)
        return operation_obj

    @property
    def worker(self):
        return self.request.user.worker

    def create(self, request, *args, **kwargs):
        data = request.data
        done_serializer = PublicOperationDoneSerializer(data=data)
        if done_serializer.is_valid():
            amount = done_serializer.data.get('amount')
            worker_operation = get_object_or_404(WorkerOperation, worker=self.worker, operation=self.get_object())
            worker_operation.operation_done(amount)

            operation_response = PublicOperationListSerializer(self.get_object(), context={'request': request}).data
            return Response(operation_response, status=HTTP_200_OK)
        return Response(done_serializer.errors, status=HTTP_400_BAD_REQUEST)


class PublicWorkerDetail(GenericAPIView):
    permission_classes = [IsAuthenticatedWorker]

    def get_object(self):
        try:
            return self.request.user.worker
        except AttributeError:
            raise Http404

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return PublicWorkerUpdateSerializer
        return PublicWorkerDetailSerializer

    def get(self, request, *args, **kwargs):
        worker = self.get_object()
        serializer = self.get_serializer_class()
        worker_serializer = serializer(worker).data
        return Response(worker_serializer, status=HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        data = request.data
        worker = self.get_object()
        serializer = self.get_serializer_class()
        worker_serializer = serializer(worker, data=data)
        if worker_serializer.is_valid():
            worker_serializer.save()
            response_data = PublicWorkerDetailSerializer(worker).data
            return Response(response_data, status=HTTP_200_OK)
        return Response(worker_serializer.errors, status=HTTP_400_BAD_REQUEST)


class StartWorking(APIView):
    permission_classes = [IsAuthenticatedWorker]

    def post(self, request, *args, **kwargs):
        worker = self.worker
        if not worker.is_working:
            worker.start_working()
            return Response(status=HTTP_200_OK)
        return Response(data={'error': 'Is working now.'}, status=HTTP_400_BAD_REQUEST)

    @property
    def worker(self):
        return self.request.user.worker


class StopWorking(APIView):
    permission_classes = [IsAuthenticatedWorker]

    def post(self, request, *args, **kwargs):
        worker = self.worker
        if worker.is_working:
            worker.stop_working()
            return Response(status=HTTP_200_OK)
        return Response(data={'error': 'Does not working now.'}, status=HTTP_400_BAD_REQUEST)

    @property
    def worker(self):
        return self.request.user.worker