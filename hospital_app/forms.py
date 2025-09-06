from django import forms
from .models import Doctor, Patient, Appointment, Treatment, Bill

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name','specialization','phone','email']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name','gender','dob','phone','address']
        widgets = {
            'dob': forms.DateInput(attrs={'type':'date'})
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient','doctor','appointment_date','diagnosis']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type':'datetime-local'})
        }

class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = ['appointment','treatment_description','medicine_prescribed']

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['appointment','total_amount','payment_status']
