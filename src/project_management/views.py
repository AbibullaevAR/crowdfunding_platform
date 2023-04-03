from rest_framework import generics
from rest_framework import permissions

from project_management.models import Category, Project
from project_management.serializers import CreateProjectSerializer, CategorySerializer, RetrieveProjectSerializer

# Create your views here.

class CreateProjectView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CreateProjectSerializer

    def perform_create(self, serializer: CreateProjectSerializer):
        serializer.save(author=self.request.user, **serializer.validated_data)


class RetrieveProjectView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = RetrieveProjectSerializer

    def get_object(self) -> Project:
        project_id = self.request.GET.get('id')
        return Project.objects.get(id=project_id)


class ListCategoryView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()