from django.urls import path

from .views import (
    CreateProjectView, 
    ListCategoryView, 
    RetrieveProjectView, 
    LikeProjectView, 
    ChangeProjectStatusView,
    ListApproveProjectView,
    ListUserProjectView
    )

app_name = 'project_management'

urlpatterns = [
    path("create_project/",  CreateProjectView.as_view(), name="create_project"),
    path("retrieve_project/", RetrieveProjectView.as_view(), name="retrieve_project"),
    path("list_project/", ListApproveProjectView.as_view(), name="list_project"),
    path("list_user_project/", ListUserProjectView.as_view(), name="list_user_project"),
    path("like_project/", LikeProjectView.as_view(), name="like_project"),
    path("list_category/", ListCategoryView.as_view(), name="list_category"),

    # Admin path
    path('change_status/<uuid:id>/', ChangeProjectStatusView.as_view(), name='change_status')
]