from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# User = settings.AUTH_USER_MODEL

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """User model."""

    username = None
    email = models.EmailField('Email', unique=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)  # Add the is_active field
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Add any required fields here (e.g., first_name, last_name)

    objects = UserManager()


class YTTasker(models.Model):
    y_user = models.ForeignKey(User, related_name="YTtask_user", on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)
    momo_number = PhoneNumberField(null=False, blank=False)
    def __str__(self):
        return self.y_user.email
    
class Profile(models.Model):
    yttasker = models.ForeignKey(YTTasker, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    momo_number = PhoneNumberField(null=False, blank=False)
    password = models.CharField(max_length=50)
    phonenumber = PhoneNumberField(null=False, blank=False)

    def __str__(self):
        return f"{self.yttasker} - {self.password}"

    @receiver(post_save, sender=YTTasker)
    def create_yttasker_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(
                yttasker=instance,
                username="",  # Set the username value if necessary
                email=instance.email,  # Use the email attribute of YTTasker
                momo_number=instance.momo_number,
                password=instance.password,  # Set the password value if necessary
                phonenumber="",  # Set the phonenumber value if necessary
            )
