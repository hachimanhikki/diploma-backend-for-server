from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import api.model.models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.


class MyTeachertManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Teacher(AbstractBaseUser):
    email = models.EmailField(verbose_name="email",
                              max_length=200, unique=True)
    username = models.CharField(max_length=200, unique=True)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=200)
    second_name = models.CharField(max_length=200)
    position = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)
    kpi = models.CharField(max_length=200, null=True)
    one_rate = models.IntegerField(null=True)
    load = models.FloatField(null=True)
    total_hour = models.IntegerField(default=0)
    department = models.ForeignKey(
        api.model.models.Department, null=True, on_delete=models.SET_NULL)

    USERNAME_FIELD = 'username'

    objects = MyTeachertManager()

    def __str__(self) -> str:
        return f"{self.id} {self.first_name} {self.second_name} {self.total_hour}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
