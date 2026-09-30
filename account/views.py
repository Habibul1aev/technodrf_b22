import random
from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import RegisterSerializer, LoginSerializer, ProfileSerializer, UserUpdateSerializer, VerifyOTPCodeSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import OTPCode, User
from core.settings import EMAIL_HOST_USER


class Register(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            code = str(random.randint(100000, 999999))

            OTPCode.objects.filter(email=email).delete()

            OTPCode.objects.create(email=email, code=code)

            send_mail(
                subject='Ваш код подтверждения',
                message=f'Ваш код: {code}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[email]
            )

            return Response({'message': 'Мы отправили код'}, status=status.HTTP_200_OK)


        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class VerifyCode(APIView):
    def post(self, request):
        serializer = VerifyOTPCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            phone = serializer.validated_data['phone']
            otp = serializer.validated_data['otp']

            user = User.objects.create_user(
                email=email,
                username=email,
                password=password,
                phone=phone
            )

            otp.delete()

            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'message': 'User was created with token',
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)




class Login(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'message': 'User was created with token',
                'token': token.key
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = ProfileSerializer(request.user)

        return Response(serializer.data)

    def patch(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)





class ResetPasswordRequest(APIView):

    def post(self, request):
        serializer = ResetPasswordRequestSerializer(
            data=request.data
        )

        if serializer.is_valid():
            email = serializer.validated_data['email']

            code = str(random.randint(100000, 999999))

            OTPCode.objects.filter(email=email).delete()

            OTPCode.objects.create(
                email=email,
                code=code
            )

            send_mail(
                subject='Восстановление пароля',
                message=f'Ваш код: {code}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[email]
            )

            return Response({
                'message': 'Код восстановления отправлен на email'
            })

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ResetPasswordVerify(APIView):

    def post(self, request):
        serializer = ResetPasswordVerifySerializer(
            data=request.data
        )

        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']
            otp = serializer.validated_data['otp']

            user = User.objects.get(email=email)

            user.set_password(new_password)
            user.save()

            otp.delete()

            Token.objects.filter(user=user).delete()

            return Response({
                'message': 'Пароль успешно изменён'
            })

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )