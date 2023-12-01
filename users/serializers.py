from rest_framework import serializers

from study_platform.serializers import PaymentsSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Сериалайзер для пользователя """
    payments_history = serializers.SerializerMethodField()

    def get_payments_history(self, instance):
        payments = instance.user.all()
        return PaymentsSerializer(payments, many=True).data

    class Meta:
        model = User
        fields = ('email', 'password', 'city', 'payments_history')


class UserShortSerializer(serializers.ModelSerializer):
    """ Сериалайзер для вывода только публичной информации """

    class Meta:
        model = User
        fields = ('first_name', 'email', 'city')