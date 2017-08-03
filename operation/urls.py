from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from operation import views

urlpatterns = format_suffix_patterns([
    url(r'^$', views.ProductOperationList.as_view(), name='operation-list'),
    url(r'^(?P<operation_id>\d+)/$', views.ProductOperationDetail.as_view(), name='operation-detail'),
])
