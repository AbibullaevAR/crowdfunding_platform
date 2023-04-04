from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.request import Request

from project_management.models import Category, Project
from project_management.serializers import CreateProjectSerializer, CategorySerializer, RetrieveProjectSerializer, LikeProjectSerializer
from project_management.services import like_project

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


class LikeProjectView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = LikeProjectSerializer

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        like_project(serializer.validated_data.get('project_id'), request.user)

        return Response(status=status.HTTP_202_ACCEPTED)
