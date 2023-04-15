from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions

from .serializers import CreateUserSerializer, RetrieveUserSerializer, UpdateUserStatusSerializer
from .services import CreateUserService
from accounts.services import ConfirmEmailService
from accounts.permissions import IsAdmin

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
    

class RetrieveUserView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = RetrieveUserSerializer

    def get_object(self):
        return self.request.user


class ListUserView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    serializer_class = RetrieveUserSerializer
    queryset = get_user_model().objects.all()

    def filter_queryset(self, queryset):
        email = self.request.GET.get('email')

        if email:
            return queryset.filter(email=email)
        
        return queryset


class UpdateUserStatusView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    serializer_class = UpdateUserStatusSerializer

    def get_object(self):
        return get_user_model().objects.get(id=self.kwargs['id'])