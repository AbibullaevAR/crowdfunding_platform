from rest_framework import serializers

from project_management.models import Project, Category
from attached_file.models import Image


class CreateProjectSerializer(serializers.ModelSerializer):

    images = serializers.ListField(child=serializers.ChoiceField(Image.AVAILABLE_FORMAT_CHOICES), source='images.all')
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)

    class Meta:
        model = Project
        fields = ('title', 'goal_likes', 'short_description', 'start_project', 'end_project', 'categories', 'images')


class ProjectSerializer(serializers.ModelSerializer):

    img_links = serializers.SerializerMethodField()
    
    taken_likes = serializers.IntegerField(source='taken_likes_count')
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)

    class Meta:
        model = Project
        fields = ('id', 'taken_likes', 'title', 'goal_likes', 'short_description', 'start_project', 'end_project', 'categories', 'img_links')
    
    def get_img_links(self, project):
        context = self.get_context(project)
        return context.get('img_links')
    
    def get_context(self, project: Project) -> dict:

        if isinstance(self.context, list):
            project_id = project.id
            return [item.get(project_id) for item in self.context if project_id in item][0]
        
        return self.context.get(project.id)

    @staticmethod
    def create_context(project: Project, data) -> dict:
        return {project.id: data}

class ChangeProjectStatusSerializer(serializers.ModelSerializer):

    status = serializers.ChoiceField(choices=Project.STATUS_CHOICES)

    class Meta:
        model = Project
        fields = ('status', )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')


class LikeProjectSerializer(serializers.Serializer):
    project_id = serializers.UUIDField()
    