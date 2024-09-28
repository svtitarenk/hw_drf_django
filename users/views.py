from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.serializers import UserSerializer


# Create your views here.
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
