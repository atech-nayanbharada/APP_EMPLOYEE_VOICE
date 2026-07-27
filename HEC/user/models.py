from django.db import models

# Create your models here.

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager


# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    create custom user model
    """

    HR_EXECUTIVE='hr_executive'
    HR_MANAGER = 'hr_manager'
    ADMIN = 'admin'
    USER_TYPE = ((HR_EXECUTIVE, "HR_Executive"), (HR_MANAGER, "HR_Manager"),(ADMIN, "Admin"))
    full_name = models.CharField(max_length=500)
    email = models.EmailField(unique=True, error_messages={
        "unique": "This email address is already associated with another account."
    }, )
    user_type = models.CharField(max_length=50, choices=USER_TYPE, default=HR_EXECUTIVE)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}"

    def user_data(self):
        """
        This data used  for user data
        """
        return f"{self.full_name}+{self.email}"
