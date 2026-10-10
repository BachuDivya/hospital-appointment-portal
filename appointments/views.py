
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from .models import Doctor, Patient, Appointment
from .forms import SignupForm, AppointmentForm


def home(request):
    doctors = Doctor.objects.filter(available=True)
    specialty = request.GET.get('specialty', '')
    search = request.GET.get('search', '')

    if specialty:
        doctors = doctors.filter(specialty=specialty)

    if search:
        doctors = doctors.filter(name__icontains=search)

    return render(request, 'appointments/home.html', {
        'doctors': doctors,
        'specialties': Doctor.SPECIALTIES,
        'selected_specialty': specialty,
        'search': search,
    })


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignupForm()

    return render(request, 'appointments/signup.html', {'form': form})


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard')

    return render(request, 'appointments/login.html', {'form': form})


@login_required
def book_appointment(request):
    patient, created = Patient.objects.get_or_create(
    user=request.user,
    defaults={
        'phone': '0000000000',
        'address': ''
    }
)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            try:
                appointment.save()
                messages.success(request, 'Appointment booked successfully.')
                return redirect('dashboard')
            except Exception:
                form.add_error(
                    None,
                    'This time slot may have just been booked. Please try another.'
                )
    else:
        form = AppointmentForm()

    return render(request, 'appointments/book_appointment.html', {
        'form': form
    })


@login_required
def dashboard(request):
    patient = Patient.objects.filter(user=request.user).first()
    appointments = (
        Appointment.objects.filter(patient=patient)
        if patient else Appointment.objects.none()
    )
    return render(request, 'appointments/dashboard.html', {
        'appointments': appointments
    })


def staff_required(user):
    return user.is_staff


@user_passes_test(staff_required)
def manage_appointments(request):
    appointments = Appointment.objects.select_related(
        'doctor', 'patient', 'patient__user'
    ).all()

    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        status = request.POST.get('status')
        valid_statuses = dict(Appointment.STATUS_CHOICES)

        if status in valid_statuses:
            appointment = get_object_or_404(
                Appointment, pk=appointment_id
            )
            appointment.status = status
            appointment.save()
            messages.success(request, 'Appointment status updated.')
        else:
            messages.error(request, 'Invalid appointment status.')

        return redirect('manage_appointments')

    return render(request, 'appointments/manage_appointments.html', {
        'appointments': appointments,
        'statuses': Appointment.STATUS_CHOICES,
    })

