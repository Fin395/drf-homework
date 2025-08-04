import stripe
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from users.models import Payments, User
from users.permissions import IsProfileOwner
from users.serializers import (
    PaymentsSerializer,
    UserSerializer,
    UserReducedSerializer,
)
from rest_framework.permissions import IsAuthenticated

from users.services import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_session,
    get_status,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsProfileOwner]


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson", "paying_method")
    ordering_field = "payment_date"


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user == self.get_object():
            return UserSerializer
        return UserReducedSerializer


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserReducedSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer

    def perform_create(self, serializer):
        payment = serializer.save(
            user=self.request.user,
            amount=serializer.validated_data["paid_course"].price,
        )
        product = create_stripe_product(payment.paid_course)
        price = create_stripe_price(payment.amount, product)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class PaymentStatusAPIView(APIView):
    @swagger_auto_schema(
        request_body=PaymentsSerializer,
        responses={200: "Success"},
    )
    def get(self, *args, **kwargs):
        session_id = self.request.data.get("session_id")
        try:
            payment_status = get_status(session_id)
            return Response({"статус платежа": payment_status})
        except stripe.error.CardError as e:
            return Response({"error": str(e)})
