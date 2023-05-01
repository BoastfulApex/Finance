from django.db import models
from django.contrib.auth.models import User
from .managers import *
import uuid


class FinUser(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(primary_key=True, default=uuid.uuid4, blank=False, unique=True, editable=False,
                               max_length=500, name=("id"), verbose_name=("User ID"))
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, name=("phone"), null=True, blank=True)
    telegram_id = models.CharField(max_length=15, unique=True, name=("telegram_id"), null=True, blank=True)
    email = models.EmailField(db_index=True, unique=True, name=("email"))
    image = models.ImageField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False) 
    # new_phone = models.CharField(max_length=15, null=True, blank=True) 
    # otp = models.CharField(max_length=10, null=True)
    # otp_expire = models.DateTimeField(auto_now_add=False, null=True)
    
    USERNAME_FIELD = 'email'   #by default it takes username. but we  change  to  email
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return "{}".format(self.email)

    # def check_otp_expire(self, date):
    #     if date <= self.otp_expire.replace(tzinfo=None):
    #         return True
    #     if date > self.otp_expire.replace(tzinfo=None):
    #         return False


    class Meta:
        db_table = 'FinUser'
        verbose_name = "User"
        managed = True

