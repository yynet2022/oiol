# -*- coding: utf-8 -*-
import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser


class MyUserManager(BaseUserManager):
    REQUIRED_FIELDS = ["uid"]

    def create_user(self, uid, **kwargs):
        if not uid:
            raise ValueError('Users must have an UID')
        user = self.model(uid=uid.lower())
        user.username = uid.upper()  # char150, Unique=True
        # first_name = char150, blank=True
        # last_name = char150, blank=True
        # email = blank=True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = False

        user.set_password(None)
        user.save(using=self._db)
        return user

    def create_superuser(self, uid, **kwargs):
        user = self.create_user(uid)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uid = models.CharField(
        verbose_name='User ID',
        max_length=10,
        unique=True,
    )
    objects = MyUserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.uid

    def __str__(self):
        return 'User<{},{}>'.format(self.uid, self.is_superuser)
