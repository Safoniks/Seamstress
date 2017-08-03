from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = format_suffix_patterns([
    url(r'^admin/$', views.UserCreate.as_view(), name='admin'),
    url(r'^worker/$', views.UserCreate.as_view(), name='worker'),
])
