from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The given mobile_number must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_staff', False)
        # extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(mobile_number, password, **extra_fields)


class User(AbstractUser):
    user_permissions = None
    groups = None
    is_staff = None
    last_login = None
    is_superuser = None
    first_name = None
    last_name = None
    date_joined = None
    mobile_number = models.CharField(max_length=15,unique=True)
    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = []
    id = models.AutoField(primary_key=True)
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(max_length=50)
    profile_photo = models.FileField(null=True)
    email_token = models.CharField(max_length=300,null=True)
    otp_expiry = models.DateTimeField(null=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.mobile_number

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
           # 'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class AuthUser(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    otp = models.PositiveIntegerField(null=True)
    otp_expiry = models.DateTimeField(null=True)
    email_token = models.CharField(max_length=300,null=True)
    email_token_expiry = models.DateTimeField(null=True)
    is_otpvalidated = models.BooleanField(default=False,null=True)
