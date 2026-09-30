from django.contrib.auth.models import UserManager as BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):

        user = self.model(
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password=None, **extra_fields):

        user = self.create_user(
            username=username,
            password=password,
            **extra_fields
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user