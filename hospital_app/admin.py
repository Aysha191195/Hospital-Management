from django.contrib import admin
from .models import Doctor, Patient, Appointment, Treatment, Bill

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'phone')
    search_fields = ('name', 'specialization', 'phone')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'phone')
    search_fields = ('name', 'phone')
    list_filter = ('gender',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time')
    list_filter = ('date', 'doctor')


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'patient', 'doctor', 'date')
    search_fields = ('name', 'patient__name', 'doctor__name')
    list_filter = ('date',)


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('patient', 'amount', 'status', 'date')
    search_fields = ('patient__name',)
    list_filter = ('status', 'date')
