from rest_framework import serializers

from project_management.models import Project, Category
from attached_file.models import Image


class CreateProjectSerializer(serializers.ModelSerializer):

    images = serializers.ListField(child=serializers.ChoiceField(Image.AVAILABLE_FORMAT_CHOICES), source='images.all')
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)

    class Meta:
        model = Project
        fields = ('title', 'goal_likes', 'short_description', 'start_project', 'end_project', 'categories', 'images')


class RetrieveProjectSerializer(serializers.ModelSerializer):

    img_links = serializers.SerializerMethodField()
    
    taken_likes = serializers.IntegerField(source='taken_likes_count')
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)

    class Meta:
        model = Project
        fields = ('id', 'taken_likes', 'title', 'goal_likes', 'short_description', 'start_project', 'end_project', 'categories', 'img_links')
    
    def get_img_links(self, instance):
        return self.context.get('img_links')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')


class LikeProjectSerializer(serializers.Serializer):
    project_id = serializers.UUIDField()
    