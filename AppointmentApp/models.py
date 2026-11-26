
from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


# Les différents statuts d'un rendez-vous
class Status(models.TextChoices):
    PENDING = 'PENDING', 'En attente'
    CONFIRMED = 'CONFIRMED', 'Confirmé'
    CANCELLED = 'CANCELLED', 'Annulé'


# Modèle Appointment
class Appointment(models.Model):

    reason = models.TextField()

    prescription = models.FileField(
        upload_to='prescriptions/',
        blank=True,
        validators=[FileExtensionValidator(['pdf'])]
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    duration_minutes = models.PositiveIntegerField(default=30)

    appointment_date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    doctor = models.ForeignKey(
        'AccountApp.Doctor',
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    patient = models.ForeignKey(
        'AccountApp.Patient',
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    def clean(self):
        super().clean()

        if self.appointment_date:
            old_date = None

            if self.pk:
                old_date = type(self).objects.filter(
                    pk=self.pk
                ).values_list(
                    'appointment_date',
                    flat=True
                ).first()

            # Vérifier uniquement à la création
            # ou lorsque la date est modifiée
            if old_date != self.appointment_date:
                if self.appointment_date <= timezone.now():
                    raise ValidationError({
                        'appointment_date':
                        "Le rendez-vous doit être dans le futur."
                    })
                
    def clean(self):
            modified_date=self._state.adding or (Appointment.objects.filter(pk=self.pk,appointment_date=self.appointment_date).exists())
            if self.appointment_date <= timezone.now():
                raise ValidationError( "Le rendez-vous doit être supérieur à la date d'aujourd'hui.")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_doctor_appointment_date'
            )
        ]

        ordering = ['appointment_date']



    def __str__(self):
        return (
            f"{self.patient} - {self.doctor} "
            f"- {self.appointment_date}"
        )
    def __str__(self):
        return f"le rdv est pour la raison {self.reason}"

