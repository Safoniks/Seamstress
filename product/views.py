from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveDestroyAPIView,
)

from .models import Product, ProductPhoto
from .serializers import (
    ProductSerializer,
    ProductPhotoSerializer,
    ProductPhotosCreateSerializer,
    ProductOperationsCreateUpdateSerializer,
    ProductPhotosUpdateSerializer,
)


class ProductList(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        photos = request.data.get('photos', None)
        photo_files = dict(request.FILES).get('photos', None)
        operations = request.data.get('operations', None)
        product_serializer = ProductSerializer(data=data)

        if product_serializer.is_valid():
            is_valid = True
            product = product_serializer.save()
            serialized_product = product_serializer.data
        else:
            is_valid = False
            product = None
            serialized_product = {}
        product_serializer_errors = product_serializer.errors
        serializer_context = {'product': product}

        if photos:
            photos_serializer = ProductPhotosCreateSerializer(
                data={'photos': photo_files},
                context=serializer_context
            )

            if photos_serializer.is_valid() and is_valid:
                photos_serializer.save()
                serialized_product['photos'] = photos_serializer.context['photos']
            else:
                is_valid = False
                product_serializer_errors.update(photos_serializer.errors)

        if operations:
            operations_serializer = ProductOperationsCreateUpdateSerializer(
                data={'operations': operations},
                context=serializer_context
            )

            if operations_serializer.is_valid() and is_valid:
                operations_serializer.save()
                serialized_product['operations'] = operations_serializer.context['operations']
            else:
                is_valid = False
                product_serializer_errors.update(operations_serializer.errors)

        if is_valid:
            return Response(serialized_product, status=HTTP_201_CREATED)
        else:
            product and product.delete()
            return Response(product_serializer_errors, status=HTTP_400_BAD_REQUEST)


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

    def update(self, request, *args, **kwargs):
        data = request.data
        product = self.product
        serializer_context = {'product': product}
        new_photos = request.data.get('photos', [])
        new_operations = request.data.get('operations', [])

        product_serializer = ProductSerializer(product, data=data)
        photos_serializer = ProductPhotosUpdateSerializer(
            product.photos,
            data={'photos': new_photos},
            context=serializer_context
        )
        operations_serializer = ProductOperationsCreateUpdateSerializer(
            product.operations,
            data={'operations': new_operations},
            context=serializer_context
        )

        validated = (
            product_serializer.is_valid(),
            photos_serializer.is_valid(),
            operations_serializer.is_valid(),
        )
        if False not in validated:
            product_serializer.save()
            photos_serializer.save()
            operations_serializer.save()
            serialized_product = product_serializer.data
            serialized_product['photos'] = photos_serializer.context['photos']
            serialized_product['operations'] = operations_serializer.context['operations']
            return Response(serialized_product, status=HTTP_201_CREATED)
        else:
            product_serializer_errors = product_serializer.errors
            product_serializer_errors.update(photos_serializer.errors)
            product_serializer_errors.update(operations_serializer.errors)
            return Response(product_serializer_errors, status=HTTP_400_BAD_REQUEST)

    @property
    def product(self):
        product_id = self.kwargs.get(self.lookup_url_kwarg)
        product = get_object_or_404(Product, id=product_id)
        return product


class ProductPhotoList(ListCreateAPIView):
    serializer_class = ProductPhotoSerializer
    parser_classes = (MultiPartParser, FormParser)
    lookup_url_kwarg = 'product_id'

    def create(self, request, *args, **kwargs):
        photos = dict(request.FILES).get('photos')
        serializer_context = {'product': self.product}
        photos_serializer = ProductPhotosCreateSerializer(data={'photos': photos}, context=serializer_context)
        if photos_serializer.is_valid():
            photos_serializer.save()
            photos = photos_serializer.context['photos']
            return Response(photos, status=HTTP_201_CREATED)
        return Response(photos_serializer.errors, status=HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset_list = ProductPhoto.active_objects.filter(product=self.product)
        return queryset_list

    @property
    def product(self):
        product_id = self.kwargs.get(self.lookup_url_kwarg)
        product = get_object_or_404(Product, id=product_id)
        return product


class ProductPhotoDetail(RetrieveDestroyAPIView):
    queryset = ProductPhoto.active_objects.all()
    serializer_class = ProductPhotoSerializer
    lookup_url_kwarg = 'photo_id'
