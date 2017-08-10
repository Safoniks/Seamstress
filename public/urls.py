from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = format_suffix_patterns([
    url(r'^worker/$', views.PublicWorkerDetail.as_view(), name='worker-detail'),
    url(r'^worker/operation/$', views.PublicOperationList.as_view(), name='operation-list'),
    url(r'^worker/operation/(?P<operation_id>\d+)/$', views.PublicOperationDetail.as_view(), name='operation-detail'),
    url(r'^worker/operation/(?P<operation_id>\d+)/done/$', views.PublicOperationDone.as_view(), name='operation-done'),
    url(r'^worker/timer/$', views.TimerDetail.as_view(), name='timer-detail'),
    url(r'^worker/timer/start/$', views.StartTimer.as_view(), name='start-timer'),
    url(r'^worker/timer/stop/$', views.StopTimer.as_view(), name='stop-timer'),
    url(r'^worker/timer/reset/$', views.ResetTimer.as_view(), name='reset-timer'),
])
