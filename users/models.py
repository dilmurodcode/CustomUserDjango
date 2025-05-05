from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

NEW, ACTIVE = ('New', 'Active')


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_field):
        if not phone:
            raise ValueError('Phone is required')

        user = self.model(phone=phone, **extra_field)
        user.set_password(password)
        user.save(using=self.db)
        return user


    def create_superuser(self, phone, password=None, **extra_field):
        extra_field.setdefault('is_staff', True)
        extra_field.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_field)


class CustomUser(AbstractUser):

    STATUS_CHOICES = [
        (NEW, "New"),
        (ACTIVE, "Active")
    ]

    username = None
    first_name = None
    last_name = None
    email = None

    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=NEW)
    phone = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, null=True)


    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "CustomUser"

    def save(self, *args, **kwargs):

        if not self.password.startswith("pbkdf2_sha256"):
            self.set_password(self.password)

        super().save(*args, **kwargs)

    def tokens(self):
        refresh =RefreshToken.for_user(self)
        return {
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
        }


class CodeVerification(BaseModel):
    code = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, related_name='code_verifies', on_delete=models.CASCADE)
    expire_date = models.DateTimeField()

    objects = models.Manager()


