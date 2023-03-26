from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import CreateUserView, ConfirmEmailView

app_name = 'accounts'

urlpatterns = [
    path("create_user/", CreateUserView.as_view(), name="create_user"),
    path('confirm_email/<token>', ConfirmEmailView.as_view(), name='confirm_email'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]