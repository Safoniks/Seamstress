from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = format_suffix_patterns([
    url(r'^$', views.WorkerList.as_view(), name='worker-list'),
    url(r'^(?P<worker_id>\d+)/$', views.WorkerDetail.as_view(), name='worker-detail'),
    url(r'^(?P<worker_id>\d+)/operation/$', views.WorkerOperationList.as_view(), name='worker-operation-list'),
    url(r'^(?P<worker_id>\d+)/operation/(?P<operation_id>\d+)/$', views.WorkerOperationDetail.as_view(), name='worker-operation-detail'),
])
