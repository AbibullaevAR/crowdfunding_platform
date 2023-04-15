from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .views import CreateUserView, ConfirmEmailView, RetrieveUserView, ListUserView

app_name = 'accounts'

urlpatterns = [
    path("create_user/", CreateUserView.as_view(), name="create_user"),
    path("retrieve_user/", RetrieveUserView.as_view(), name="retrieve_user"),
    path("users/", ListUserView.as_view(), name="users_list"),
    path('confirm_email/<token>', ConfirmEmailView.as_view(), name='confirm_email'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify")
]