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
    ListAPIView
)

from .models import Worker
from .serializers import (
    WorkerSerializer,
)


class WorkerList(ListAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
