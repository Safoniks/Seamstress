from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from operation import views

urlpatterns = format_suffix_patterns([
    url(r'^$', views.ProductOperationList.as_view(), name='operation-list'),
    # url(r'^(?P<product_id>\d+)/$', views.ProductDetail.as_view(), name='product-detail'),
    # url(r'^(?P<product_id>\d+)/photo/$', views.ProductPhotoList.as_view(), name='product-photo-list'),
    # url(r'^(?P<product_id>\d+)/photo/(?P<pk>\d+)$', views.ProductPhotoDetail.as_view(), name='product-photo-detail'),
])
