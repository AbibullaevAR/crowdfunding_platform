from django.urls import path

from .views import (
    CreateProjectView, 
    ListCategoryView, 
    RetrieveProjectView,
    DeleteProjectView, 
    LikeProjectView, 
    ChangeProjectStatusView,
    ListApproveProjectView,
    ListUserProjectView,
    ListWaitingProjectView,
    LikedByUserView,
    CreateCommentView,
    ListCommentProjectView,
    DeleteCommentView
    )

app_name = 'project_management'

urlpatterns = [
    path("create_project/",  CreateProjectView.as_view(), name="create_project"),
    path("delete_project/<uuid:id>/", DeleteProjectView.as_view(), name="delete_project"),
    path("retrieve_project/", RetrieveProjectView.as_view(), name="retrieve_project"),
    path("list_project/", ListApproveProjectView.as_view(), name="list_project"),
    path("list_user_project/", ListUserProjectView.as_view(), name="list_user_project"),
    path("like_project/", LikeProjectView.as_view(), name="like_project"),
    path("list_category/", ListCategoryView.as_view(), name="list_category"),
    path("liked-by-user/", LikedByUserView.as_view(), name="liked-by-user"),
    path("create_comment/", CreateCommentView.as_view(), name="create_comment"),
    path("delete_comment/<uuid:id>/", DeleteCommentView.as_view(), name="delete_comment"),
    path("project_comment/", ListCommentProjectView.as_view(), name="project_comment"),

    # Admin path
    path('list_waiting_project/', ListWaitingProjectView.as_view(), name="list_waiting_project"),
    path('change_status/<uuid:id>/', ChangeProjectStatusView.as_view(), name='change_status')
]