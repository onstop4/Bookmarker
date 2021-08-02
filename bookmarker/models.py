from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not (email and password):
            raise ValueError("Invalid values for email or password")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_confirmed", True)

        if kwargs.get("is_staff") is not True or kwargs.get("is_superuser") is not True:
            raise ValueError("Invalid values for is_staff or is_superuser")
        return self.create_user(email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=256, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    datetime_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    objects = UserManager()


class EmailConfirmationToken(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="email_confirm_token",
    )
    token = models.CharField(max_length=100)

    def __str__(self):
        return self.token


class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lists")
    name = models.CharField(max_length=300)

    def delete_related_bookmarks(self):
        self.bookmarks.all().delete()

    def __str__(self):
        return self.name


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    name = models.CharField(max_length=300)
    url = models.URLField(max_length=2000)
    unread = models.BooleanField(default=True)
    datetime_created = models.DateTimeField(default=timezone.now)
    list = models.ForeignKey(
        List, null=True, on_delete=models.SET_NULL, related_name="bookmarks"
    )

    def __str__(self):
        return self.name
