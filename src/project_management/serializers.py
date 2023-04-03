from rest_framework import serializers

from project_management.models import Project, ProjectCategory, Category


class CreateProjectSerializer(serializers.ModelSerializer):

    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)

    class Meta:
        model = Project
        fields = ('title', 'goal_likes', 'short_description', 'start_project', 'end_project', 'categories')


class RetrieveProjectSerializer(serializers.ModelSerializer):
    
    taken_likes = serializers.IntegerField(source='taken_likes_count')
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)

    class Meta:
        model = Project
        fields = ('id', 'taken_likes', 'title', 'goal_likes', 'short_description', 'start_project', 'end_project', 'categories')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')