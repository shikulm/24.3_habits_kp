from rest_framework import serializers

from courses.models import Payment
# from courses.serializers import PaymentSerialaizer
from users.models import User
from courses.models import Payment

class PaymentSerialaizerForUser(serializers.ModelSerializer):
    class Meta:
        model = Payment
        # fields = '__all__'
        fields = ("id", "date_pay", "course", "lesson", "payment_amount", "payment_method")



class UserSerialaizer(serializers.ModelSerializer):

    payments = PaymentSerialaizerForUser(many=True, read_only=True)

    class Meta:
        model = User
        # fields = '__all__'
        fields = ("id", "email", "phone", "city", "payments")



