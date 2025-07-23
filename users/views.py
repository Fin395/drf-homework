from rest_framework import generics
from users.models import User, Payments
from users.serializers import UserSerializer, PaymentsSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'paying_method')
    ordering_field = ('payment_date')


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
