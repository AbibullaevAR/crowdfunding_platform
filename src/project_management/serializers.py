from rest_framework import serializers

from project_management.models import Project, ProjectCategory, Category


class CreateProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('title', 'goal_likes', 'short_description', 'start_project', 'end_project', 'categories')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')