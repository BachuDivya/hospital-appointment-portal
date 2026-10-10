
from django.contrib import admin
from .models import Doctor, Patient, Appointment, MedicalReport


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'qualification', 'experience', 'available')
    list_filter = ('specialty', 'available')
    search_fields = ('name', 'specialty')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'time_slot', 'status')
    list_filter = ('status', 'appointment_date')
    search_fields = ('patient__user__username', 'doctor__name')


@admin.register(MedicalReport)
class MedicalReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'patient', 'report_date')



