from django.shortcuts import render
from hospital_app.models import Doctor, Patient, Appointment  # <-- use hospital_app

def home(request):
    context = {
        'doctors_count': Doctor.objects.count(),
        'patients_count': Patient.objects.count(),
        'appointments_count': Appointment.objects.count(),
    }
    return render(request, 'home.html', context)
