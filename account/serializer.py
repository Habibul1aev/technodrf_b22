from rest_framework import serializers
from account.models import User, OTPCode
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Пользователь с таким email существует')

        return value


class VerifyOTPCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    code = serializers.CharField(max_length=6)
    phone = serializers.CharField()

    def validate(self, attrs):
        email = attrs['email']
        code = attrs['code']

        otp = OTPCode.objects.filter(email=email, code=code).first()

        if not otp:
            raise serializers.ValidationError({'message': 'Такой код не найден'})

        if otp.is_expired():
            otp.delete()

            raise serializers.ValidationError({'message': 'Срок истек'})

        attrs['otp'] = otp

        return attrs




class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):

        user = authenticate(
            username=attrs['username'],
            password=attrs['password']
        )

        if user is None:
            raise serializers.ValidationError(
                'Неверный username или пароль'
            )

        attrs['user'] = user

        return attrs



class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['password']


class DataUserSerializer(serializers.Serializer):
    username = serializers.CharField()


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'phone', 'email', 'avatar', 'first_name', 'last_name']


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email не найден'
            )

        return value


class ResetPasswordVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=6)

    def validate(self, attrs):
        email = attrs['email']
        code = attrs['code']

        otp = OTPCode.objects.filter(
            email=email,
            code=code
        ).first()

        if not otp:
            raise serializers.ValidationError({
                'message': 'Такой код не найден'
            })

        if otp.is_expired():
            otp.delete()

            raise serializers.ValidationError({
                'message': 'Срок действия кода истёк'
            })

        attrs['otp'] = otp

        return attrs