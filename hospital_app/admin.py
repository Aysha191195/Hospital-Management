
# Register your models here.

from django.contrib import admin
from .models import Patient, Doctor, Appointment, Treatment, Bill

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id','name','gender','dob','phone')
    search_fields = ('name','phone','address')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id','name','specialization','phone','email')
    search_fields = ('name','specialization')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id','patient','doctor','appointment_date','diagnosis')
    list_filter = ('doctor','appointment_date')
    search_fields = ('patient__name','doctor__name','diagnosis')

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('id','appointment','treatment_description','medicine_prescribed')

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('id','appointment','total_amount','payment_status')
    list_filter = ('payment_status',)
