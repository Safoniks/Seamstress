from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    GenericAPIView,
)

from operation.models import Operation
from worker.models import WorkerOperation
from public.models import WorkerTiming

from .serializers import (
    PublicOperationListSerializer,
    PublicOperationDoneSerializer,
    PublicWorkerDetailSerializer,
    PublicWorkerUpdateSerializer,
    TimerDetailSerializer,
    RatingDoneDailySerializer,
    WorkerGoalSerializer,
)
from .permissions import IsAuthenticatedWorker

from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class PublicWorkerDetail(GenericAPIView):
    # authentication_classes = (JSONWebTokenAuthentication,)
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


class PublicOperationList(ListAPIView):
    # authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = PublicOperationListSerializer
    permission_classes = [IsAuthenticatedWorker]

    def get_queryset(self):
        queryset_list = Operation.objects.filter(worker=self.worker)
        return queryset_list

    @property
    def worker(self):
        return self.request.user.worker


class PublicOperationDetail(RetrieveAPIView):
    # authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = PublicOperationListSerializer
    permission_classes = [IsAuthenticatedWorker]
    lookup_url_kwarg = 'operation_id'

    def get_object(self):
        operation_id = self.kwargs.get(self.lookup_url_kwarg)
        operation_obj = get_object_or_404(Operation, worker=self.worker, id=operation_id)
        return operation_obj

    @property
    def worker(self):
        return self.request.user.worker


class PublicOperationDone(CreateAPIView):
    # authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = PublicOperationDoneSerializer
    permission_classes = [IsAuthenticatedWorker]
    lookup_url_kwarg = 'operation_id'

    def get_object(self):
        operation_id = self.kwargs.get(self.lookup_url_kwarg)
        operation_obj = get_object_or_404(Operation, worker=self.worker, id=operation_id)
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

            worker_detail_response = PublicWorkerDetailSerializer(self.worker, context={'request': request}).data
            return Response(worker_detail_response, status=HTTP_200_OK)
        return Response(done_serializer.errors, status=HTTP_400_BAD_REQUEST)


class TimerDetail(GenericAPIView):
    # authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = TimerDetailSerializer
    permission_classes = [IsAuthenticatedWorker]

    def get_object(self):
        try:
            return self.request.user.worker
        except AttributeError:
            raise Http404

    def get(self, request, *args, **kwargs):
        worker = self.get_object()
        serializer = self.serializer_class

        timer_serializer = serializer(worker).data
        return Response(timer_serializer, status=HTTP_200_OK)


class StartTimer(APIView):
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [IsAuthenticatedWorker]

    def post(self, request, *args, **kwargs):
        worker = self.worker
        if not worker.is_working:
            worker.timer_do(WorkerTiming.START)
            return Response(status=HTTP_200_OK)
        return Response(data={
            'detail': "Is working now."
        }, status=HTTP_400_BAD_REQUEST)

    @property
    def worker(self):
        return self.request.user.worker


class StopTimer(APIView):
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [IsAuthenticatedWorker]

    def post(self, request, *args, **kwargs):
        worker = self.worker
        if worker.is_working:
            worker.timer_do(WorkerTiming.STOP)
            return Response(status=HTTP_200_OK)
        return Response(data={
            'detail': "Does not working now."
        }, status=HTTP_400_BAD_REQUEST)

    @property
    def worker(self):
        return self.request.user.worker


class ResetTimer(APIView):
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [IsAuthenticatedWorker]

    def post(self, request, *args, **kwargs):
        worker = self.worker
        if not worker.is_working:
            worker.timer_do(WorkerTiming.RESET)
            return Response(status=HTTP_200_OK)
        return Response(data={
            'detail': "Is working now."
        }, status=HTTP_400_BAD_REQUEST)

    @property
    def worker(self):
        return self.request.user.worker


class RatingDoneDaily(GenericAPIView):
    # authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = RatingDoneDailySerializer
    permission_classes = [IsAuthenticatedWorker]

    def get_object(self):
        try:
            return self.request.user.worker
        except AttributeError:
            raise Http404

    def get(self, request, *args, **kwargs):
        worker = self.get_object()
        serializer = self.serializer_class

        rating_serializer = serializer(worker).data
        return Response(rating_serializer, status=HTTP_200_OK)


class WorkerGoal(GenericAPIView):
    # authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = WorkerGoalSerializer
    permission_classes = [IsAuthenticatedWorker]

    def get_object(self):
        try:
            return self.request.user.worker
        except AttributeError:
            raise Http404

    def get(self, request, *args, **kwargs):
        worker = self.get_object()
        serializer = self.serializer_class

        if worker.goal:
            goal_serializer = serializer(worker.goal).data
            return Response(goal_serializer, status=HTTP_200_OK)
        else:
            raise Http404

    def post(self, request, *args, **kwargs):
        data = request.data
        worker = self.get_object()
        serializer = self.serializer_class

        if worker.goal:
            return Response({
                "detail": "Goal already exist."
            }, status=HTTP_400_BAD_REQUEST)
        else:
            goal_serializer = serializer(data=data)
            if goal_serializer.is_valid():
                goal = goal_serializer.save()
                worker.goal = goal
                worker.save()
                return Response(goal_serializer.data, status=HTTP_201_CREATED)
            else:
                return Response(goal_serializer.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        data = request.data
        worker = self.get_object()
        serializer = self.serializer_class

        if worker.goal:
            goal_serializer = serializer(worker.goal, data=data)
            if goal_serializer.is_valid():
                goal_serializer.save()
                return Response(goal_serializer.data, status=HTTP_201_CREATED)
            else:
                return Response(goal_serializer.errors, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "detail": "Goal does not exist."
            }, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        worker = self.get_object()
        if worker.goal:
            worker.goal.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        else:
            return Response({
                "detail": "Goal does not exist."
            }, status=HTTP_400_BAD_REQUEST)
