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

# from .models import Product, ProductPhoto
# from .serializers import (
#     ProductSerializer,
#     ProductPhotoSerializer,
#     ProductPhotosCreateSerializer,
# )


# class ProductPhotoList(ListCreateAPIView):
#     serializer_class = ProductPhotoSerializer
#     parser_classes = (MultiPartParser, FormParser)
#     lookup_url_kwarg = 'product_id'
#
#     def create(self, request, *args, **kwargs):
#         product_id = self.kwargs.get(self.lookup_url_kwarg)
#         photos = dict(request.FILES).get('photo')
#         photos_serializer = ProductPhotosCreateSerializer(data={
#             'photo': photos,
#             'product_id': product_id
#         })
#         if photos_serializer.is_valid(raise_exception=True):
#             photos_serializer.save()
#             return Response(status=HTTP_201_CREATED)
#         return Response(photos_serializer.errors, status=HTTP_400_BAD_REQUEST)
#
#     def get_queryset(self):
#         queryset_list = ProductPhoto.objects.filter(product=self.product)
#         return queryset_list
#
#     @property
#     def product(self):
#         product_id = self.kwargs.get(self.lookup_url_kwarg)
#         product = get_object_or_404(Product, id=product_id)
#         return product


