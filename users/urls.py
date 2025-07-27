from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.apps import UsersConfig
from users.views import (PaymentsListAPIView, UserRetrieveAPIView,
                         UserUpdateAPIView, UserCreateAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path("user/register/", UserCreateAPIView.as_view(), name="user-register"),
    path("user/update/<int:pk>/", UserUpdateAPIView.as_view(), name="user-update"),
    path("payments/", PaymentsListAPIView.as_view(), name="payments-list"),
    path("user/<int:pk>/", UserRetrieveAPIView.as_view(), name="user-get"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
