import json

from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.request import Request

from accounts.permissions import IsAdmin
from project_management.models import Category, Project
from project_management.serializers import CreateProjectSerializer, CategorySerializer, RetrieveProjectSerializer, LikeProjectSerializer, ChangeProjectStatusSerializer
from project_management.services import like_project
from attached_file.services import create_image_for_project, get_download_link_for_images

# Create your views here.

class CreateProjectView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CreateProjectSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        available_formats = serializer.validated_data.pop('images')['all']

        project = serializer.save(author=self.request.user, **serializer.validated_data)

        resp_data = {
            'upload_links': create_image_for_project(project=project, available_formats=available_formats)
        }

        headers = self.get_success_headers(serializer.data)
        return Response(resp_data, status=status.HTTP_201_CREATED, headers=headers)


class RetrieveProjectView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = RetrieveProjectSerializer

    def get_object(self) -> Project:
        project_id = self.request.GET.get('id')
        return Project.objects.get(id=project_id)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        img_links = get_download_link_for_images(instance.images.all())

        serializer = self.get_serializer(instance, context={'img_links': img_links})
        return Response(serializer.data)


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


class ChangeProjectStatusView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    serializer_class = ChangeProjectStatusSerializer

    def get_object(self):
        return Project.objects.get(id=self.kwargs['id'])

    