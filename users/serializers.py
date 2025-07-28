from rest_framework import serializers

from users.models import Payments, User


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    payments_history = PaymentsSerializer(source="payments", many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }


class UserReducedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'city', 'is_staff']
