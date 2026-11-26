
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MinLengthValidator,
    RegexValidator
)
from django.core.exceptions import ValidationError
from django.utils import timezone


# Modèle User
class User(AbstractUser):
    pass


# Modèle Specialty
class Specialty(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "Specialties"
        verbose_name = "Specialty"


# Modèle Doctor
class Doctor(User):

    license_number = models.CharField(
        max_length=6,
        unique=True,
        validators=[MinLengthValidator(6)]
    )
    phone = models.CharField(
        max_length=8,
        validators=[RegexValidator(r'^\d{8}$')]
    )
    specialties = models.ManyToManyField(Specialty)
    class Meta:
            verbose_name_plural ="Doctors"
            verbose_name = "Doctor"

# Validateur de date de naissance
def validate_past_date(value):
    if value >= timezone.localdate():
        raise ValidationError(
            "La date de naissance doit être antérieure à aujourd'hui."
        )


# Modèle Patient
class Patient(User):

    national_id = models.CharField(
        max_length=8,
        unique=True,
        validators=[RegexValidator(r'^\d{8}$')]
    )

    phone = models.CharField(
        max_length=8,
        validators=[RegexValidator(r'^\d{8}$')]
    )

    birth_date = models.DateField(
        validators=[validate_past_date]
    )
    class Meta:
        verbose_name_plural = "Patients"
        verbose_name = "Patient"



