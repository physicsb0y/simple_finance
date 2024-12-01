from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import UserManager
from apps.utils.abstract_model import TimeStampModel

# Create your models here.

class Address(TimeStampModel):
    country = models.CharField(max_length=25)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    street = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.country}, {self.province}, {self.city}, {self.zip_code}, {self.street or ''}"



class User(AbstractUser, TimeStampModel):
    email = models.EmailField(unique=True)
    phone_numbers = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    citizenship_number = models.CharField(max_length=25, null=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.DO_NOTHING, null=True, blank=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_numbers', 'date_of_birth', 'citizenship_number']
    objects = UserManager()

    def __str__(self):
        return f"{self.get_full_name()} - {self.email}"
