from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = format_suffix_patterns([
    url(r'^$', views.WorkerList.as_view(), name='worker-list'),
    url(r'^(?P<worker_id>\d+)/$', views.WorkerDetail.as_view(), name='worker-detail'),
    # url(r'^(?P<product_id>\d+)/photo/$', views.ProductPhotoList.as_view(), name='product-photo-list'),
    # url(r'^(?P<product_id>\d+)/photo/(?P<photo_id>\d+)$', views.ProductPhotoDetail.as_view(), name='product-photo-detail'),
])

# urlpatterns += [url(r'^(?P<product_id>\d+)/operation/', include('operation.urls', namespace='operation')), ]
