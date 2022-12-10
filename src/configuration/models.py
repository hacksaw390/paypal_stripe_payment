from django.db import models
from base.models import BaseModel
# Create your models here.


class TermsAndConditions(BaseModel):
    header = models.CharField(max_length=150, unique=True)
    conditions = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.header



class AboutUs(BaseModel):
    header = models.CharField(max_length=150, unique=True)
    details = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.header