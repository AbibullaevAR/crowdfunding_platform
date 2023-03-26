from rest_framework import generics

from .serializers import CreateUserSerializer
from .services import CreateUserService

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer

    def perform_create(self, serializer):
        CreateUserService().execute(**serializer.validated_data)