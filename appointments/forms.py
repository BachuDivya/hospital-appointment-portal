
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import Patient, Appointment


class SignupForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            Patient.objects.create(
                user=user,
                phone=self.cleaned_data['phone']
            )

        return user


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'doctor', 'appointment_date', 'time_slot', 'reason'
        ]
        widgets = {
            'appointment_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = (
            self.fields['doctor'].queryset.filter(available=True)
        )

    def clean_appointment_date(self):
        date = self.cleaned_data['appointment_date']
        if date < timezone.localdate():
            raise forms.ValidationError(
                'Appointment date cannot be in the past.'
            )
        return date

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        date = cleaned_data.get('appointment_date')
        slot = cleaned_data.get('time_slot')

        if doctor and date and slot:
            existing = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=date,
                time_slot=slot
            ).exclude(status='Cancelled')

            if existing.exists():
                raise forms.ValidationError(
                    'This time slot is already booked. Please choose another.'
                )

        return cleaned_data
