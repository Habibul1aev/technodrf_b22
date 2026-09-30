from django.contrib.auth.models import AbstractUser
from django.db import models
from account.manager import UserManager
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


    phone = models.CharField(
        max_length=20,
        blank=True
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []



class OTPCode(models.Model):
    class Meta:
        verbose_name = 'OTPcode'
        verbose_name_plural = 'OTPcode'

    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()


    def save(self, *args, **kwargs):
        if not self.expired_at:
            self.expired_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expired_at

    def __str__(self):
        return self.email

        