from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=150)
    gender = models.CharField(max_length=10, choices=(('Male','Male'),('Female','Female'),('Other','Other')))
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=150)
    specialization = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.specialization})"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField(null=True, blank=True)
    diagnosis = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.patient.name} → {self.doctor.name} @ {self.appointment_date:%Y-%m-%d %H:%M}"

class Treatment(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='treatments')
    treatment_description = models.TextField()
    medicine_prescribed = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f"Treatment for {self.appointment}"

class Bill(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='bills')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    PAYMENT_STATUS_CHOICES = (('Paid','Paid'), ('Pending','Pending'))
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Bill {self.id} - {self.appointment.patient.name} - {self.total_amount}"
