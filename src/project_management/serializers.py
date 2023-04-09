from rest_framework import serializers

from project_management.models import Project, Category
from attached_file.models import Image


class CategorySerializer(serializers.ModelSerializer):

    text = serializers.CharField(source='name')

    class Meta:
        model = Category
        fields = ('id', 'text')


class CreateProjectSerializer(serializers.ModelSerializer):

    images = serializers.ListField(child=serializers.ChoiceField(Image.AVAILABLE_FORMAT_CHOICES), source='images.all')
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)

    class Meta:
        model = Project
        fields = ('title', 'goal_likes', 'short_description', 'start_project', 'end_project', 'categories', 'images')


class ProjectSerializer(serializers.ModelSerializer):

    images = serializers.SerializerMethodField()
    
    taken_likes = serializers.IntegerField(source='taken_likes_count')
    categories = CategorySerializer(many=True)

    class Meta:
        model = Project
        fields = ('id', 'taken_likes', 'title', 'goal_likes', 'short_description', 'start_project', 'end_project', 'categories', 'images')
    
    def get_images(self, project: Project):
        return project.get_images()


class ChangeProjectStatusSerializer(serializers.ModelSerializer):

    status = serializers.ChoiceField(choices=Project.STATUS_CHOICES)

    class Meta:
        model = Project
        fields = ('status', )


class LikeProjectSerializer(serializers.Serializer):
    project_id = serializers.UUIDField()
    