from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import OperationTypeCategoryViewSet

operation_type_category_list = OperationTypeCategoryViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
operation_type_category_detail = OperationTypeCategoryViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    url(r'^$', operation_type_category_list, name='operation-type-category-list'),
    url(r'^(?P<operation_type_category_id>\d+)/$', operation_type_category_detail, name='operation-type-category-detail')
])
