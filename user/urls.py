from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = format_suffix_patterns([
    url(r'^worker/$', views.WorkerCreate.as_view(), name='register-worker'),
    url(r'^technologist/$', views.TechnologistCreate.as_view(), name='register-technologist'),
    url(r'^director/$', views.DirectorCreate.as_view(), name='register-director'),
])
