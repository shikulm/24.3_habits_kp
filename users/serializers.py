from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации пользователя"""
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['telegram', 'password', 'password2']

    def validate(self, attrs):
        """Проверка совпадаения паролей"""
        data = super().validate(attrs)
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Пароли не совпадают')
        del data['password2']
        return data

    def create(self, validated_data):
        user = User(telegram=validated_data['telegram'])
        user.set_password(validated_data['password'])
        user.save()
        return user


    # def update(self, user, validated_data):
    #     user.name = validated_data['name']
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

