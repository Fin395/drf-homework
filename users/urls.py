from django.urls import path

from users.apps import UsersConfig
from users.views import (PaymentsListAPIView, UserRetrieveAPIView,
                         UserUpdateAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path("user/update/<int:pk>/", UserUpdateAPIView.as_view(), name="user-update"),
    path("payments/", PaymentsListAPIView.as_view(), name="payments-list"),
    path("user/<int:pk>/", UserRetrieveAPIView.as_view(), name="user-get"),
]
