from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """Create and return a superuser with an email, password, and admin rights."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    subscription = models.ForeignKey('Subscription', on_delete=models.SET_NULL, null=True, blank=True)

    objects = UserManager()

    def __str__(self):
        return self.username

class Subscription(models.Model):
    SUBSCRIPTION_TYPES = [
        ('FREE', 'Free'),
        ('BASIC', 'Basic'),
        ('PREMIUM', 'Premium'),
    ]

    subscription_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=10, choices=SUBSCRIPTION_TYPES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.type} Subscription ({self.subscription_id})"
