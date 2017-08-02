from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import OperationTypeViewSet

operation_type_list = OperationTypeViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
operation_type_detail = OperationTypeViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    url(r'^$', operation_type_list, name='operation-type-list'),
    url(r'^(?P<pk>\d+)/$', operation_type_detail, name='operation-type-detail')
])
