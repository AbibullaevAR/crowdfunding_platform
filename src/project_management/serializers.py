from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from project_management.models import Project, Category, Comment
from attached_file.models import Image
from accounts.serializers import RetrieveUserSerializer


class CategorySerializer(serializers.ModelSerializer):

    text = serializers.CharField(source='name')

    class Meta:
        model = Category
        fields = ('id', 'text')


class AuthorSerializer(serializers.ModelSerializer):

    projects = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'id', 'projects', 'is_admin', 'created_at')

    def get_projects(self, author):
        return len(author.projects.filter(status='approve').all())


class CreateUpdateProjectSerializer(serializers.ModelSerializer):

    images = serializers.ListField(child=serializers.ChoiceField(Image.AVAILABLE_FORMAT_CHOICES), source='images.all')
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)

    class Meta:
        model = Project
        fields = ('title', 'goal_likes', 'short_description', 'description', 'start_project', 'end_project', 'categories', 'images')
    
    def validate(self, attrs):
        if attrs['start_project'] < timezone.localdate():
            raise ValidationError(_('Start date should be greater or equal to current date.'))
        if attrs['start_project'] > attrs['end_project']:
            raise ValidationError(_('End date should be greater or equal to start date.'))
        
        return attrs


class ProjectSerializer(serializers.ModelSerializer):

    images = serializers.SerializerMethodField()
    
    taken_likes = serializers.IntegerField(source='taken_likes_count')
    categories = CategorySerializer(many=True)
    author = AuthorSerializer()

    class Meta:
        model = Project
        fields = ('id', 'taken_likes', 'title', 'goal_likes', 'short_description', 'description', 'start_project', 'end_project', 'categories', 'images', 'status', 'author')
    
    def get_images(self, project: Project):
        return self.context['images'].get(project.id)


class ChangeProjectStatusSerializer(serializers.ModelSerializer):

    status = serializers.ChoiceField(choices=Project.STATUS_CHOICES)

    class Meta:
        model = Project
        fields = ('status', )


class LikeProjectSerializer(serializers.Serializer):
    project_id = serializers.UUIDField()


class LikedByUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', )


class CreateCommentSerializer(serializers.ModelSerializer):

    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.filter(status='approve').all())

    class Meta:
        model = Comment
        fields = ('text', 'project')


class CommentSerializer(serializers.ModelSerializer):

    user = RetrieveUserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'created_at', 'user')
        