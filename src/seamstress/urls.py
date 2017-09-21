from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_swagger.views import get_swagger_view

from user.urls import settings_urlpatterns


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'register-worker': reverse('core:register-worker', request=request, format=format),
        'register-technologist': reverse('core:register-technologist', request=request, format=format),
        'register-director': reverse('core:register-director', request=request, format=format),
        'login-admin': reverse('core:login-admin', request=request, format=format),
        'login-worker': reverse('public:login-worker', request=request, format=format),

        'settings': reverse('core:settings', request=request, format=format),

        'products': reverse('core:product-list', request=request, format=format),
        'operation-types': reverse('core:operation-type-list', request=request, format=format),
        'operation-type-categories': reverse('core:operation-type-category-list', request=request, format=format),
        'workers': reverse('core:worker-list', request=request, format=format),
        'brigades': reverse('core:brigade-list', request=request, format=format),

        'public-worker': reverse('public:worker-detail', request=request, format=format),
        'public-worker-goal': reverse('public:worker-goal', request=request, format=format),
        'public-worker-rating': reverse('public:worker-rating', request=request, format=format),
        'public-worker-operations': reverse('public:operation-list', request=request, format=format),

        'timer': reverse('public:timer-detail', request=request, format=format),
        'start-timer': reverse('public:start-timer', request=request, format=format),
        'stop-timer': reverse('public:stop-timer', request=request, format=format),
        'reset-timer': reverse('public:reset-timer', request=request, format=format),
    })


core_urlpatterns = [
    url(r'^product/', include('product.urls')),
    url(r'^operation-type/', include('operationtype.urls')),
    url(r'^operation-type-category/', include('operationtypecategory.urls')),
    url(r'^worker/', include('worker.urls')),
    url(r'^brigade/', include('brigade.urls')),

    url(r'^settings/', include(settings_urlpatterns)),

    url(r'^register/', include('user.urls')),
    url(r'^login/$', obtain_jwt_token, name='login-admin'),
]


urlpatterns = [
    url(r'^schema/', get_swagger_view(title='Seamstress API')),

    url(r'^admin/', admin.site.urls),

    url(r'^accounts/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^api/v1/$', api_root),
    url(r'^api/v1/core/', include(core_urlpatterns, namespace='core')),
    url(r'^api/v1/public/', include('public.urls', namespace='public')),
]
