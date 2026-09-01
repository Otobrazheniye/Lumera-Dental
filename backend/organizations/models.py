from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.utils.text import slugify
from django.utils import timezone

from django.db import transaction
from django.db.models import Q

from django.conf import settings


# User
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)
    

class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    company = models.CharField(max_length=150, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email



# Dent
class Organization(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Membership(models.Model):
    ROLE_ADMIN = "admin"
    ROLE_DOCTOR = "doctor"
    ROLE_RECEPTIONIST = "receptionist"
    ROLE_CONTENT_MANAGER = "content_manager"

    ROLE_CHOICES = [
        (ROLE_ADMIN, "Admin"),
        (ROLE_DOCTOR, "Doctor"),
        (ROLE_RECEPTIONIST, "Receptionist"),
        (ROLE_CONTENT_MANAGER, "Content manager"),
    ]


    clinic = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="clinic_memberships",)
    role = models.CharField(max_length=40, choices=ROLE_CHOICES,)

    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["clinic", "user"],
                # One user can be added to the same clinic only once.
                name="unique_clinic_user_membership",
            )
        ]

    
    def __str__(self):
        return f"{self.user.email} -> {self.clinic.name}"
    #1 Membership: Membership object (1) - уже меняется на -> #2
    #2 <Membership: doctor@test.com -> Lumera Dental Prague>

# TEXT CHOICES Membership 
# class Role(models.TextChoices):
#     ADMIN = "admin", "Admin"
#     DOCTOR = "doctor", "Doctor"
#     RECEPTIONIST = "receptionist", "Receptionist"
#     CONTENT_MANAGER = "content_manager", "Content Manager"

# class Membership(models.Model):
# ..
# role = models.CharField(max_length=30, choices=Role.choices,)

