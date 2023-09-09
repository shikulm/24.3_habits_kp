from rest_framework import serializers

from courses.models import Payment
from users.models import User
from courses.models import Payment

class PaymentSerialaizerForUser(serializers.ModelSerializer):
    """Сериалайзер по оплате за обучение. Используется для включения в сериализвтор с пользователями."""
    class Meta:
        model = Payment
        # fields = '__all__'
        fields = ("id", "date_pay", "course", "lesson", "payment_amount", "payment_method")



class UserSerialaizer(serializers.ModelSerializer):
    """Сериалайзер для пользователя (используется для вывода детальной информации для пользователя о себе).
    Выводит поля по пользователяю ("id", "email", "phone", "city", "payments")
    и по оплате пользователем курсов и уроков"""
    payments = PaymentSerialaizerForUser(many=True, read_only=True)

    class Meta:
        model = User
        # fields = '__all__'
        fields = ("id", "email", "password", "last_name", "phone", "city", "payments")

class UserOtherSerialaizer(serializers.ModelSerializer):
    """Сериалайзер для вывода основных данных про другим пользователям.
    Выводит поля по пользователяю ("id", "email", "phone", "city", "payments")
    и по оплате пользователем курсов и уроков"""

    class Meta:
        model = User
        # fields = '__all__'
        fields = ("id", "email", "phone", "city")

