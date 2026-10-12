from django.db import migrations


def seed_data(apps, schema_editor):
    Doctor = apps.get_model('appointments', 'Doctor')
    User = apps.get_model('auth', 'User')
    Patient = apps.get_model('appointments', 'Patient')
    Appointment = apps.get_model('appointments', 'Appointment')

    doctors_data = [
        {
            "id": 1,
            "name": "Dr. Priya Sharma",
            "specialty": "Cardiology",
            "qualification": "MBBS, MD",
            "experience": 8,
            "available": True,
        },
        {
            "id": 2,
            "name": "Sindhu",
            "specialty": "Pediatrics",
            "qualification": "MBBS",
            "experience": 2,
            "available": True,
        },
        {
            "id": 3,
            "name": "Divya",
            "specialty": "Orthopedics",
            "qualification": "MBBS",
            "experience": 3,
            "available": True,
        },
        {
            "id": 4,
            "name": "Rajani",
            "specialty": "Neurology",
            "qualification": "MBBS, MD",
            "experience": 5,
            "available": True,
        },
        {
            "id": 5,
            "name": "Dr. Priya Sharma",
            "specialty": "Cardiology",
            "qualification": "MBBS, MD",
            "experience": 5,
            "available": True,
        },
    ]

    for d in doctors_data:
        if not Doctor.objects.filter(id=d["id"]).exists():
            Doctor.objects.create(**d)

    # Create admin user if not exists
    admin_user = User.objects.filter(username="admin").first()
    if not admin_user:
        admin_user = User.objects.create(
            username="admin",
            email="divyabachu9@gmail.com",
            password="pbkdf2_sha256$1000000$xf4c3eKQvnS0WxuKkmx0Wb$I7ZxPlFeAsBhgYXlL5sU7uBx9x0IS9DTECfpiE39W74=",
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

    # Create patient profile for admin if not exists
    patient = Patient.objects.filter(user=admin_user).first()
    if not patient:
        patient = Patient.objects.create(
            user=admin_user,
            phone="0000000000",
            address="",
        )

    # Sample appointments
    sample_appointments = [
        {
            "id": 1,
            "doctor_id": 1,
            "patient_id": patient.id,
            "appointment_date": "2026-10-18",
            "time_slot": "09:00",
            "reason": "General health checkup",
            "status": "Pending",
        },
        {
            "id": 2,
            "doctor_id": 1,
            "patient_id": patient.id,
            "appointment_date": "2026-10-19",
            "time_slot": "09:00",
            "reason": "Fever",
            "status": "Confirmed",
        },
        {
            "id": 3,
            "doctor_id": 1,
            "patient_id": patient.id,
            "appointment_date": "2026-10-18",
            "time_slot": "10:00",
            "reason": "General health checkup",
            "status": "Pending",
        },
        {
            "id": 4,
            "doctor_id": 3,
            "patient_id": patient.id,
            "appointment_date": "2026-10-18",
            "time_slot": "09:00",
            "reason": "Bone injury",
            "status": "Pending",
        },
        {
            "id": 5,
            "doctor_id": 2,
            "patient_id": patient.id,
            "appointment_date": "2026-10-18",
            "time_slot": "09:00",
            "reason": "Fever",
            "status": "Pending",
        },
    ]

    for appt in sample_appointments:
        if not Appointment.objects.filter(id=appt["id"]).exists():
            Appointment.objects.create(**appt)


def unseed_data(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_data, unseed_data),
    ]
