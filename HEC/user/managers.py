"""
This file is used for creating custom user manager for the correspondent custom user.
"""
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Class for creating custom manager for managing custom user.
    """

    def create_user(
            self,
            email=None,
            full_name=None,
            password=None,
            **extra_fields
    ):
        """
        Function for creating user w.r.t custom user.
        """
        user = self.model(email=self.normalize_email(email))
        user.full_name = full_name
        user.is_superuser = False
        user.is_active = True
        user.is_staff = False

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, email, password):
        """
        Function for creating super user.
        """
        user = self.create_user(
            email,
            full_name,
            password,
        )
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user

