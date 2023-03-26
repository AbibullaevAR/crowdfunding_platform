from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import generics
from rest_framework.views import APIView

from .serializers import CreateUserSerializer
from .services import CreateUserService
from accounts.services import ConfirmEmailService

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer

    def perform_create(self, serializer):
        CreateUserService().execute(view=self, **serializer.validated_data)
    
    def get_absolute_uri(self, local_url: str, **kwargs) -> str:
        return self.request.build_absolute_uri(reverse(local_url, kwargs=kwargs))


class ConfirmEmailView(APIView):
    def get(self, request, token):
        redirect_url = ConfirmEmailService().execute(token=token)
        return HttpResponseRedirect(redirect_to=redirect_url)