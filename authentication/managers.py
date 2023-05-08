from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, password=None, **kwargs):

        if first_name is None:
            raise TypeError('Users must have a First Name')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(first_name=first_name, email=email, **kwargs)
        user.is_active = True
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        # if password is None:
        #     raise TypeError('Superusers must have a password.')

        # user = self.create_user(phone, password, last_name='User')
        # user.is_superuser = True
        # user.is_staff = True
        # user.is_active = True
        # user.save()

        # return user

        if not email:
            raise ValueError('Users must have an phone.')

        user = self.model(
            first_name='Super',
            last_name='User',
            email=email,
            is_staff=True,
            is_superuser=True,

        )

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user
