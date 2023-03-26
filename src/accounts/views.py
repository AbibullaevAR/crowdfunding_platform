from django.http import HttpResponseRedirect
from rest_framework import generics
from rest_framework.views import APIView

from .serializers import CreateUserSerializer
from .services import CreateUserService
from accounts.services import ConfirmEmailService

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer

    def perform_create(self, serializer):
        CreateUserService().execute(**serializer.validated_data)


class ConfirmEmailView(APIView):
    def get(self, request, token):
        redirect_url = ConfirmEmailService().execute(token=token)
        return HttpResponseRedirect(redirect_to=redirect_url)