from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = format_suffix_patterns([
    url(r'^$', views.BrigadeList.as_view(), name='brigade-list'),
    url(r'^(?P<brigade_id>\d+)/$', views.BrigadeDetail.as_view(), name='brigade-detail'),
])
