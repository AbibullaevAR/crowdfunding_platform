from django.urls import path

from .views import CreateProjectView, ListCategoryView

app_name = 'project_management'

urlpatterns = [
    path("create_project/",  CreateProjectView.as_view(), name="create_project"),
    path("list_category/", ListCategoryView.as_view(), name="list_category")
]