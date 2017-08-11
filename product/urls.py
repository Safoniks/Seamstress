from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from product import views

urlpatterns = format_suffix_patterns([
    url(r'^$', views.ProductList.as_view(), name='product-list'),
    url(r'^(?P<product_id>\d+)/$', views.ProductDetail.as_view(), name='product-detail'),
    url(r'^(?P<product_id>\d+)/photo/$', views.ProductPhotoList.as_view(), name='product-photo-list'),
    url(r'^(?P<product_id>\d+)/photo/(?P<photo_id>\d+)$', views.ProductPhotoDetail.as_view(), name='product-photo-detail'),
])

urlpatterns += [url(r'^(?P<product_id>\d+)/operation/', include('operation.urls')), ]
