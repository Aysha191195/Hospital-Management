from django.shortcuts import render
from .models import Doctor, Patient, Appointment

def home(request):
    context = {
        'doctors_count': Doctor.objects.count(),
        'patients_count': Patient.objects.count(),
        'appointments_count': Appointment.objects.count(),
    }
    return render(request, 'hospital_app/home.html', context)


def patients_list(request):
    patients = Patient.objects.all()
    return render(request, 'hospital_app/patients_list.html', {'patients': patients})

