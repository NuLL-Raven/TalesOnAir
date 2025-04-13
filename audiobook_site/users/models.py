from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from core.models import AudioBook  # Changed import path to 'core.models'

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
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', default='profiles/default.jpg')
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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='profile_pictures/default_profile_picture.jpg')
    total_listening_time = models.PositiveIntegerField(default=0)
    completed_audiobooks = models.ManyToManyField(AudioBook, blank=True)
    current_streak = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username

