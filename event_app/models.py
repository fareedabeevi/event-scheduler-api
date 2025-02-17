
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import date
from django.db import models
from django.utils.timezone import now
from django.conf import settings  # Import settings for AUTH_USER_MODEL

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # Fix for conflict with reverse accessors for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='customuser_groups',  # Custom related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='customuser_permissions',  # Custom related_name
        blank=True
    )

    def __str__(self):
        return self.email


# Events Model
class Events(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="events", 
        null=True, 
        blank=True
    )
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=300)
    date = models.DateField(default=date.today, null=True)
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'events_tb'


# Sessions Model
class Sessions(models.Model):
    event = models.ForeignKey(Events, related_name='sessions', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField(default=now)  # Use timezone-aware now
    end_time = models.DateTimeField(default=now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sessions_tb'


# Speakers Model
class Speakers(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    class Meta:
        db_table = 'speakers_tb'
