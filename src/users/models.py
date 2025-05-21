
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import UserManager


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=150, verbose_name="имя")
    last_name = models.CharField(max_length=150, verbose_name="фамилия")
    middle_name = models.CharField(max_length=50, blank=True, verbose_name="отчество")
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=12, blank=True, verbose_name="номер телефона")

    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="фото профиля",
        blank=True,
        null=True
    )
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: list = []

    objects = UserManager()


    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


