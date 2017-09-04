from django.conf import settings

from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from .models import MyUser
from .serializers import (
    WorkerCreateSerializer,
    TechnologistCreateSerializer,
    DirectorCreateSerializer,
    SettingsSerializer,
)
from .permissions import IsAuthenticatedDirector, IsAuthenticatedDirectorOrTechnologist


class WorkerCreate(CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = WorkerCreateSerializer
    permission_classes = [IsAuthenticatedDirectorOrTechnologist]


class TechnologistCreate(CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = TechnologistCreateSerializer
    permission_classes = [IsAuthenticatedDirector]


class DirectorCreate(CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = DirectorCreateSerializer
    permission_classes = [IsAuthenticatedDirector]


class Settings(GenericAPIView):
    serializer_class = SettingsSerializer
    permission_classes = [IsAuthenticatedDirector]

    def get(self, request, *args, **kwargs):
        application_settings = settings.APPLICATION_SETTINGS
        return Response(application_settings, status=HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class
        settings_serializer = serializer(data=data)
        settings_serializer.is_valid(raise_exception=True)
        response = settings_serializer.save()
        return Response(response, status=HTTP_201_CREATED)
