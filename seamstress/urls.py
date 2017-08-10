"""seamstress URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

from worker.views import WorkerOperationCreate


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'register-admin': reverse('register:admin', request=request, format=format),
        'register-worker': reverse('register:worker', request=request, format=format),

        'products': reverse('product:product-list', request=request, format=format),
        'operation-types': reverse('operation-type:operation-type-list', request=request, format=format),
        'workers': reverse('worker:worker-list', request=request, format=format),
        'brigades': reverse('brigade:brigade-list', request=request, format=format),

        'set-worker-operation': reverse('create-worker-operation', request=request, format=format),

        'public-worker': reverse('public:worker-detail', request=request, format=format),
        'public-worker-operations': reverse('public:operation-list', request=request, format=format),

        'timer': reverse('public:timer-detail', request=request, format=format),
        'start-timer': reverse('public:start-timer', request=request, format=format),
        'stop-timer': reverse('public:stop-timer', request=request, format=format),
        'reset-timer': reverse('public:reset-timer', request=request, format=format),
    })


core_urlpatterns = [
    url(r'^product/', include('product.urls', namespace='product')),
    url(r'^operation-type/', include('operationtype.urls', namespace='operation-type')),
    url(r'^worker/', include('worker.urls', namespace='worker')),
    url(r'^brigade/', include('brigade.urls', namespace='brigade')),

    url(r'^set-worker-operation/$', WorkerOperationCreate.as_view(), name='create-worker-operation'),

    url(r'^register/', include('user.urls', namespace='register')),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^api/$', api_root),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^api/core/', include(core_urlpatterns)),
    url(r'^api/public/', include('public.urls', namespace='public')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
