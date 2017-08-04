from rest_framework.generics import CreateAPIView

from .models import MyUser
from .serializers import UserSerializer


class UserCreate(CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
