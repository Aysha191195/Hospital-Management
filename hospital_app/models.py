from django.db import models
from django.utils import timezone

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)  # ADD THIS

    def __str__(self):
        return self.name


class Patient(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)   # ADD THIS
    phone = models.CharField(max_length=15)
    dob = models.DateField()    # ADD THIS

    def __str__(self):
        return self.name


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.patient.name} with {self.doctor.name} on {self.date} at {self.time}"



class Treatment(models.Model):
    name = models.CharField(max_length=100)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)  # ensure exists

    def __str__(self):
        return self.name


class Bill(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # ADD THIS
    status = models.CharField(max_length=20, default="Pending")
    date = models.DateTimeField(default=timezone.now)  # ADD THIS

    def __str__(self):
        return f"{self.patient} - {self.amount}"