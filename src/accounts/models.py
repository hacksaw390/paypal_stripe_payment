from django.db import models
from django.contrib.auth.models import AbstractUser
from base.type_choices import UserRoleOption, AddressTypeChoices


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=30, choices=UserRoleOption.choices)
    profile_pic_url = models.TextField(null=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = '1. User'

    def __str__(self):
        return self.email


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=30, choices=AddressTypeChoices.choices)
    full_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    street_no = models.CharField(max_length=50)
    apartment_number = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)

    def __str__(self):
        return self.address

