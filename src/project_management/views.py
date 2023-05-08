import logging

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError

from accounts.permissions import IsAdmin
from project_management.models import Category, Project, Comment
from project_management.serializers import (
    CreateProjectSerializer,
    CategorySerializer, 
    ProjectSerializer, 
    LikeProjectSerializer, 
    ChangeProjectStatusSerializer,
    LikedByUserSerializer,
    CreateCommentSerializer,
    CommentSerializer
    )
from project_management.services import like_project, check_project_by_user_limit
from project_management.generics import ProjectListWithImageAPIView
from project_management.helpers import is_valid_uuid
from attached_file.services import create_image_for_project, get_download_link_for_images, delete_images, get_download_link_for_project_image


logger = logging.getLogger('project_management.views')


class CreateProjectView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CreateProjectSerializer

    def create(self, request, *args, **kwargs):
        logger.info('User:{user_id} start create project'.format(user_id=self.request.user.id))

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not check_project_by_user_limit(self.request.user):
            logger.exception(
                'User:{user_id} have exceeded the number of projects on consideration'.format(user_id=self.request.user.id),
                exc_info=False
            )
            raise ValidationError('you have exceeded the number of projects on consideration', status.HTTP_400_BAD_REQUEST)

        available_formats = serializer.validated_data.pop('images')['all']

        project = serializer.save(author=self.request.user, **serializer.validated_data)

        upload_links = create_image_for_project(project=project, available_formats=available_formats)

        context = {
            'images':{
                project.id: get_download_link_for_project_image(project)
            }
        }

        resp_data = {
            **ProjectSerializer(instance=project, context=context).data,
            'upload_links': upload_links
        }

        headers = self.get_success_headers(serializer.data)

        logger.info('User:{user_id} successful create project'.format(user_id=self.request.user.id))

        return Response(resp_data, status=status.HTTP_201_CREATED, headers=headers)


class UpdateProjectView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = CreateProjectSerializer

    def get_object(self):
        status_dict = dict(Project.STATUS_CHOICES)
        status_value = status_dict.get('cancel')
        
        return get_object_or_404(
            Project, 
            id=self.kwargs['id'],
            author=self.request.user,
            status=status_value
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        delete_images(instance.images.all())
        available_formats = serializer.validated_data.pop('images')['all']

        status_dict = dict(Project.STATUS_CHOICES)
        status_value = status_dict.get('waiting')

        serializer.save(status=status_value)

        upload_links = create_image_for_project(project=instance, available_formats=available_formats)

        context = {
            'images':{
                instance.id: get_download_link_for_project_image(instance)
            }
        }

        resp_data = {
            **ProjectSerializer(instance=instance, context=context).data,
            'upload_links': upload_links
        }

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(resp_data)


class DeleteProjectView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    
    def get_object(self):
        status_dict = dict(Project.STATUS_CHOICES)
        status_values = [status_dict.get('cancel'), status_dict.get('approve')]

        return get_object_or_404(
            Project, 
            id=self.kwargs['id'], 
            author=self.request.user, 
            status__in=status_values
        )
    
    def perform_destroy(self, instance):
        delete_images(instance.images.all())
        instance.delete()


class RetrieveProjectView(generics.RetrieveAPIView):
    serializer_class = ProjectSerializer

    def get_object(self) -> Project:
        project_id = self.request.GET.get('id')

        return get_object_or_404(Project, id=project_id)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        context = {
            'images':{
                instance.id: get_download_link_for_project_image(instance)
            }
        }

        serializer = self.get_serializer(instance, context=context)
        return Response(serializer.data)


class ListApproveProjectView(ProjectListWithImageAPIView):
    serializer_class = ProjectSerializer
    images_link_func = get_download_link_for_images
    
    def get_queryset(self) -> list[Project]:
        status_dict = dict(Project.STATUS_CHOICES)
        status_value = status_dict.get('approve')
        return Project.objects.filter(status=status_value).all()
    
    def filter_queryset(self, queryset):
        user_id = self.request.GET.get('userId')

        if is_valid_uuid(user_id):
            return queryset.filter(author=user_id)
        
        return queryset


class ListUserProjectView(ProjectListWithImageAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ProjectSerializer
    images_link_func = get_download_link_for_images

    def get_queryset(self):
        return Project.objects.filter(author=self.request.user).all()


class ListCategoryView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class LikeProjectView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = LikeProjectSerializer

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_id = serializer.validated_data.get('project_id')

        project = get_object_or_404(Project, id=project_id)

        like_project(project, request.user)

        return Response(status=status.HTTP_202_ACCEPTED)


class LikedByUserView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = LikedByUserSerializer

    def get_queryset(self):
        return self.request.user.project_set.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        
        resp_data = [item['id'] for item in serializer.data]

        return Response(resp_data)


class CreateCommentView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CreateCommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(user=self.request.user, **serializer.validated_data)

        headers = self.get_success_headers(serializer.data)
        return Response(CommentSerializer(instance=comment).data, status=status.HTTP_201_CREATED, headers=headers)


class DeleteCommentView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        comment_id = self.kwargs['id']
        return get_object_or_404(Comment, id=comment_id, user=self.request.user)


class ListCommentProjectView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        project_id = self.request.GET.get('id')

        status_dict = dict(Project.STATUS_CHOICES)
        status_value = status_dict.get('approve')

        project = get_object_or_404(Project, id=project_id, status=status_value)

        return Comment.objects.filter(project=project)
    

# Admin views

class ChangeProjectStatusView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    serializer_class = ChangeProjectStatusSerializer

    def get_object(self):
        return get_object_or_404(Project, id=self.kwargs['id'])


class ListWaitingProjectView(ProjectListWithImageAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    serializer_class = ProjectSerializer
    images_link_func = get_download_link_for_images

    def get_queryset(self):
        status_dict = dict(Project.STATUS_CHOICES)
        status_value = status_dict.get('waiting')
        return Project.objects.filter(status=status_value).all()

    