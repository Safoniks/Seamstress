from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import Brigade
from .serializers import (
    BrigadeSerializer,
)


class BrigadeList(ListCreateAPIView):
    queryset = Brigade.objects.all()
    serializer_class = BrigadeSerializer


class BrigadeDetail(RetrieveUpdateDestroyAPIView):
    queryset = Brigade.objects.all()
    serializer_class = BrigadeSerializer
    lookup_url_kwarg = 'brigade_id'
