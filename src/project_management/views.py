from rest_framework import generics
from rest_framework import permissions

from project_management.serializers import CreateProjectSerializer

# Create your views here.

class CreateProjectView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CreateProjectSerializer

    def perform_create(self, serializer: CreateProjectSerializer):
        serializer.save(author=self.request.user, **serializer.validated_data)
        