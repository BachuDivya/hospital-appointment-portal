from django.core.management.base import BaseCommand
from django.core.management import call_command
from appointments.models import Doctor, Patient, Appointment
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Seeds initial doctors and hospital portal data if not present'

    def handle(self, *args, **options):
        self.stdout.write('Checking hospital portal data...')

        # Try loading from fixture first if doctors table is empty
        if Doctor.objects.count() == 0:
            try:
                call_command('loaddata', 'appointments/fixtures/initial_data.json', verbosity=1)
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded fixture! Doctors count: {Doctor.objects.count()}'))
                return
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Fixture load skipped/failed ({e}), falling back to direct creation...'))

        default_doctors = [
            {'name': 'Dr. Priya Sharma', 'specialty': 'Cardiology', 'qualification': 'MBBS, MD', 'experience': 8, 'available': True},
            {'name': 'Sindhu', 'specialty': 'Pediatrics', 'qualification': 'MBBS', 'experience': 2, 'available': True},
            {'name': 'Divya', 'specialty': 'Orthopedics', 'qualification': 'MBBS', 'experience': 3, 'available': True},
            {'name': 'Rajani', 'specialty': 'Neurology', 'qualification': 'MBBS, MD', 'experience': 5, 'available': True},
        ]

        created_count = 0
        for doc in default_doctors:
            if not Doctor.objects.filter(name=doc['name'], specialty=doc['specialty']).exists():
                Doctor.objects.create(**doc)
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Seed completed. Total doctors: {Doctor.objects.count()} (New added: {created_count})'
        ))
