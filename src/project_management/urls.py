from django.urls import path

from .views import CreateProjectView

app_name = 'project_management'

urlpatterns = [
    path("create_project/",  CreateProjectView.as_view(), name="create_project")
]