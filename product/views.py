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

from mixins.mixins import MultipleFieldLookupMixin

from .models import Product, ProductPhoto
from .serializers import (
    ProductListSerializer,
    ProductPhotoSerializer,
    ProductPhotoListSerializer,
)


class ProductList(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        name = data['name']
        description = data['description']
        photos = dict(request.FILES).get('photo')
        serializer_context = {
            'request': request,
        }
        new_product = {
            'name': name,
            'description': description
        }

        product_serializer = ProductListSerializer(data=new_product, context=serializer_context)

        if product_serializer.is_valid():
            product_serializer.save()
            product = product_serializer.data

            if photos:
                photos_serializer = ProductPhotoListSerializer(data={
                    'photo': photos,
                    'product_id': product['id']
                })

                if photos_serializer.is_valid(raise_exception=True):
                    photos_serializer.save()
                    del product['photos']# photos_serializer.data = [None, ....] ?????????
                    return Response(product, status=HTTP_201_CREATED)
                else:
                    Product.objects.get(id=product['id']).delete()# invalid photos ????????????????????????????
                    return Response(photos_serializer.errors, status=HTTP_400_BAD_REQUEST)
            return Response(product, status=HTTP_201_CREATED)
        else:
            return Response(product_serializer.errors, status=HTTP_400_BAD_REQUEST)


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    lookup_url_kwarg = 'product_id'

    def destroy(self, request, *args, **kwargs):
        product_id = self.kwargs.get(self.lookup_url_kwarg)
        product_photo_dir = os.path.join(settings.MEDIA_ROOT, 'product-photos', str(product_id))
        try:
            shutil.rmtree(product_photo_dir)
        except OSError:
            pass
        return super(ProductDetail, self).destroy(request, *args, **kwargs)


class ProductPhotoList(ListCreateAPIView):
    serializer_class = ProductPhotoSerializer
    parser_classes = (MultiPartParser, FormParser)
    lookup_url_kwarg = 'product_id'

    def create(self, request, *args, **kwargs):
        product_id = self.kwargs.get(self.lookup_url_kwarg)
        photos = dict(request.FILES).get('photo')
        photos_serializer = ProductPhotoListSerializer(data={
            'photo': photos,
            'product_id': product_id
        })
        if photos_serializer.is_valid(raise_exception=True):
            photos_serializer.save()
            return Response(status=HTTP_201_CREATED)
        return Response(photos_serializer.errors, status=HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset_list = ProductPhoto.objects.filter(product=self.product)
        return queryset_list

    def perform_create(self, serializer):
        serializer.save(product=self.product)

    @property
    def product(self):
        product_id = self.kwargs.get(self.lookup_url_kwarg)
        product = get_object_or_404(Product, id=product_id)
        return product


class ProductPhotoDetail(RetrieveDestroyAPIView):
    queryset = ProductPhoto.objects.all()
    serializer_class = ProductPhotoSerializer

    def destroy(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        photo_id = self.kwargs.get('pk')
        try:
            photo = ProductPhoto.objects.filter(product__id=product_id).get(id=photo_id)
        except ObjectDoesNotExist:
            return Response(status=HTTP_400_BAD_REQUEST)

        product_photo_path = os.path.join(settings.MEDIA_ROOT, photo.photo.name)
        try:
            os.remove(product_photo_path)
        except OSError:
            pass
        return super(ProductPhotoDetail, self).destroy(request, *args, **kwargs)

