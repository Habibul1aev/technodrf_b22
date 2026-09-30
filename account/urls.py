from django.urls import path
from .views import Register, Login, ProfileAPIView, VerifyCode

urlpatterns = [
    path('register/', Register.as_view()),
    path('verify-otp/', VerifyCode.as_view() ),
    path('login/', Login.as_view()),
    path('profile/', ProfileAPIView.as_view())
]
