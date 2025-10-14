from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """
    Custom User model with email as username
    """
    username = None
    email = models.EmailField(unique=True, verbose_name='Email Address')
    full_name = models.CharField(max_length=150, blank=True, verbose_name='Full Name')
    
    # Mobile number with validation
    mobile_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    mobile = models.CharField(
        validators=[mobile_regex], 
        max_length=17, 
        blank=True,
        verbose_name='Mobile Number'
    )
    
    # Profile fields
    is_profile_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Return the full name for the user."""
        return self.full_name or self.email
    
    def get_short_name(self):
        """Return the short name for the user."""
        return self.full_name.split(' ')[0] if self.full_name else self.email.split('@')[0]
    
    def save(self, *args, **kwargs):
        # Check if profile is complete
        if self.full_name and self.mobile:
            self.is_profile_complete = True
        else:
            self.is_profile_complete = False
        super().save(*args, **kwargs)
