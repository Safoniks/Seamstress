from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = format_suffix_patterns([
    url(r'^worker/$', views.PublicWorkerDetail.as_view(), name='worker-detail'),
    url(r'^worker/operation/$', views.PublicOperationList.as_view(), name='operation-list'),
    url(r'^worker/operation/(?P<operation_id>\d+)/$', views.PublicOperationDetail.as_view(), name='operation-detail'),
    url(r'^worker/operation/(?P<operation_id>\d+)/done/$', views.PublicOperationDone.as_view(), name='operation-done'),
    url(r'^worker/start-working/$', views.StartWorking.as_view(), name='start-working'),
    url(r'^worker/stop-working/$', views.StopWorking.as_view(), name='stop-working'),
])
