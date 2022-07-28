from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
class CustomUserManager(BaseUserManager):
    
    def create_user(self, username, email, password, **other_fields):

        if not email:
            raise ValueError("Email address must be provided!!")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError("Superuser must be assign to is_staff=True")

        if other_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must be assign to is_superuser=True")

        return self.create_user(username, email, password, **other_fields)


class UsersModel(AbstractBaseUser, PermissionsMixin):

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True, blank=False)
    email = models.EmailField(_('email address'), max_length=100, unique=True, blank=False)
    password = models.CharField(max_length=100, blank=False)
    is_teacher = models.BooleanField(default=False, blank=False)
    is_staff = models.BooleanField(_("staff status"), default=False)
    profile_pic = models.CharField(max_length=100, default="Not Available", blank=False)
    created_at = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username