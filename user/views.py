from rest_framework.generics import CreateAPIView

from .models import MyUser
from .serializers import (
    WorkerCreateSerializer,
    TechnologistCreateSerializer,
    DirectorCreateSerializer,
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
