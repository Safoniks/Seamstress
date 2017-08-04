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


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'products': reverse('product:product-list', request=request, format=format),
        'operation-types': reverse('operation-type:operation-type-list', request=request, format=format),
        'register-admin': reverse('register:admin', request=request, format=format),
        'register-worker': reverse('register:worker', request=request, format=format),
        'workers': reverse('worker:worker-list', request=request, format=format),
        'brigades': reverse('brigade:brigade-list', request=request, format=format),
    })


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^api/$', api_root),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^api/register/', include('user.urls', namespace='register')),

    url(r'^api/product/', include('product.urls', namespace='product')),
    url(r'^api/operation-type/', include('operationtype.urls', namespace='operation-type')),
    url(r'^api/worker/', include('worker.urls', namespace='worker')),
    url(r'^api/brigade/', include('brigade.urls', namespace='brigade')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
