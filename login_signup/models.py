from django.db import models

# Create your models here.
class Users(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50, unique=True)
    password=models.CharField(max_length=50)
    is_verified=models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_creation_time = models.DateTimeField(auto_now=True)

class posts(models.Model):
    heading=models.CharField(max_length=50)
    author=models.CharField(max_length=50)
    description=models.CharField(max_length=500)
