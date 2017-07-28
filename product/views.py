from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.decorators import api_view
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveDestroyAPIView,
)

from mixins.mixins import MultipleFieldLookupMixin

from .models import Product, ProductPhoto
from .serializers import ProductListSerializer, ProductDetailSerializer, ProductPhotoSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'products': reverse('product:product-list', request=request, format=format),
    })


class ProductList(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     name = data['name']
    #     description = data['description']
    #     photo = data['photos.photo']
    #
    #     serializer_context = {
    #         'request': request,
    #     }
    #
    #     new_product = {
    #         'name': name,
    #         'description': description
    #     }
    #
    #     serializer = ProductListSerializer(data=new_product, context=serializer_context)
    #     print('11111111111111111111111111111', serializer)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_url_kwarg = 'product_id'


class ProductPhotoList(ListCreateAPIView):
    serializer_class = ProductPhotoSerializer
    lookup_url_kwarg = 'product_id'

    def get_queryset(self):
        product_id = self.kwargs.get(self.lookup_url_kwarg)
        product = Product.objects.get(id=product_id)
        queryset_list = ProductPhoto.objects.filter(product=product)
        return queryset_list

    def perform_create(self, serializer):
        product_id = self.kwargs.get(self.lookup_url_kwarg)
        product = Product.objects.get(id=product_id)
        serializer.save(product=product)


class ProductPhotoDetail(RetrieveDestroyAPIView):
    queryset = ProductPhoto.objects.all()
    serializer_class = ProductPhotoSerializer
