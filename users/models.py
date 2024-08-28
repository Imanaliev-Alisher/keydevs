from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):

    def _create(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Поле Email не может быть пустым.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)

        return self._create(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        return self._create(email, password, **extra_fields)


class User(AbstractBaseUser):

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=25, unique=True)
    telegram_chat_id = models.CharField(max_length=100, unique=True)
    verification_code = models.CharField(max_length=10, null=True, blank=True)
    code_expiration = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
