from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.apps import UsersConfig
from users.views import (
    PaymentsListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    UserCreateAPIView,
    UserListAPIView,
    UserDestroyAPIView,
    PaymentCreateAPIView,
    PaymentStatusAPIView,
)
from rest_framework.permissions import AllowAny


app_name = UsersConfig.name

urlpatterns = [
    path("user/register/", UserCreateAPIView.as_view(), name="user-register"),
    path("user/update/<int:pk>/", UserUpdateAPIView.as_view(), name="user-update"),
    path("payments/", PaymentsListAPIView.as_view(), name="payments-list"),
    path("user/<int:pk>/", UserRetrieveAPIView.as_view(), name="user-get"),
    path(
        "token/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("user/delete/<int:pk>/", UserDestroyAPIView.as_view(), name="user-delete"),
    path("payment/", PaymentCreateAPIView.as_view(), name="payment-create"),
    path("payment/status/", PaymentStatusAPIView.as_view(), name="payment-status-get"),
]
