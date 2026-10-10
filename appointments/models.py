from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    SPECIALTIES = [
        ('Cardiology', 'Cardiology'),
        ('Pediatrics', 'Pediatrics'),
        ('Orthopedics', 'Orthopedics'),
        ('Neurology', 'Neurology'),
    ]

    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=50, choices=SPECIALTIES)
    qualification = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.specialty}"


class Patient(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='patient_profile'
    )
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    TIME_SLOTS = [
        ('09:00', '09:00 AM'),
        ('10:00', '10:00 AM'),
        ('11:00', '11:00 AM'),
        ('14:00', '02:00 PM'),
        ('15:00', '03:00 PM'),
        ('16:00', '04:00 PM'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    time_slot = models.CharField(max_length=5, choices=TIME_SLOTS)
    reason = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date', 'time_slot'],
                name='unique_doctor_appointment_slot',
            )
        ]
        ordering = ['appointment_date', 'time_slot']

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.appointment_date}"


class MedicalReport(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(
        Appointment, on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=150)
    description = models.TextField()
    report_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

