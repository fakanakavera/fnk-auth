from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager  # Ensure the import path is correct

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    groups = models.ManyToManyField(Group, related_name='customuser_set_fnk', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set_fnk', blank=True)

    def __str__(self):
        return self.email

class UserAccountDetails(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=50)

    def __str__(self):
        return self.nick_name
