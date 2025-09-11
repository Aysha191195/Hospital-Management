from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor, Patient, Appointment, Treatment, Bill
from .forms import DoctorForm, PatientForm, AppointmentForm, TreatmentForm, BillForm, SimpleRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.core.paginator import Paginator

# Dashboard
@login_required
def home_view(request):
    context = {
        'doctors_count': Doctor.objects.count(),
        'patients_count': Patient.objects.count(),
        'appointments_count': Appointment.objects.count(),
        'treatments_count': Treatment.objects.count(),
        'bills_count': Bill.objects.count(),
    }
    return render(request, "hospital_app/home.html", context)

# ---------------- AUTH ----------------
def register_view(request):
    if request.method == "POST":
        form = SimpleRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("home")
    else:
        form = SimpleRegisterForm()
    return render(request, "registration/register.html", {"form": form})


def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, "registration/login.html", {'form': form})


def logout_view(request):
    logout(request)
    return redirect("login")

# ---------------- DOCTOR CRUD ----------------

# Doctor List with Search + Pagination
def doctor_list(request):
    query = request.GET.get("q")
    doctors = Doctor.objects.all()

    if query:
        doctors = doctors.filter(
            name__icontains=query
        ) | doctors.filter(specialization__icontains=query)

    paginator = Paginator(doctors, 5)  # 5 doctors per page
    page_number = request.GET.get("page")
    doctors_page = paginator.get_page(page_number)

    return render(request, "hospital_app/doctor_list.html", {
        "doctors": doctors_page,
        "query": query,
    })


# Add Doctor
def add_doctor(request):
    if request.method == "POST":
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("doctor_list")
    else:
        form = DoctorForm()
    return render(request, "hospital_app/add_doctor.html", {"form": form})


# Edit Doctor
def edit_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == "POST":
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect("doctor_list")
    else:
        form = DoctorForm(instance=doctor)
    return render(request, "hospital_app/edit_doctor.html", {"form": form})


# Delete Doctor
def delete_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.delete()
    return redirect('doctor_list')

# ---------------- PATIENT CRUD ----------------
def patient_list(request):
    query = request.GET.get('q', '')
    patient_list = Patient.objects.all()
    if query:
        patient_list = patient_list.filter(name__icontains=query)

    paginator = Paginator(patient_list, 10)  # 10 patients per page
    page_number = request.GET.get('page')
    patients = paginator.get_page(page_number)

    context = {
        "patients": patients,
        "query": query
    }
    return render(request, "hospital_app/patient_list.html", context)

# Add patient
def add_patient(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, "hospital_app/add_patient.html", {"form": form})


# Edit patient
def edit_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect("patient_list")
    else:
        form = PatientForm(instance=patient)
    
    # FIX: use full template path
    return render(request, "hospital_app/add_patient.html", {"form": form})

def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    patient.delete()
    return redirect("patient_list")

# ---------------- APPOINTMENT CRUD ----------------
def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, "hospital_app/appointment_list.html", {"appointments": appointments})


def add_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("appointment_list")
    else:
        form = AppointmentForm()
    return render(request, "appointment_form.html", {"form": form})

def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect("appointment_list")
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, "appointment_form.html", {"form": form})

def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    return redirect("appointment_list")

# ---------------- TREATMENT CRUD ----------------
def treatment_list(request):
    treatments = Treatment.objects.all()
    return render(request, "treatment_list.html", {"treatments": treatments})

def add_treatment(request):
    if request.method == "POST":
        form = TreatmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("treatment_list")
    else:
        form = TreatmentForm()
    return render(request, "treatment_form.html", {"form": form})

def edit_treatment(request, treatment_id):
    treatment = get_object_or_404(Treatment, id=treatment_id)
    if request.method == "POST":
        form = TreatmentForm(request.POST, instance=treatment)
        if form.is_valid():
            form.save()
            return redirect("treatment_list")
    else:
        form = TreatmentForm(instance=treatment)
    return render(request, "treatment_form.html", {"form": form})

def delete_treatment(request, treatment_id):
    treatment = get_object_or_404(Treatment, id=treatment_id)
    treatment.delete()
    return redirect("treatment_list")

# ---------------- BILL CRUD ----------------
def bill_list(request):
    bills = Bill.objects.all()
    return render(request, "bill_list.html", {"bills": bills})

def add_bill(request):
    if request.method == "POST":
        form = BillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("bill_list")
    else:
        form = BillForm()
    return render(request, "bill_form.html", {"form": form})

def edit_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    if request.method == "POST":
        form = BillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return redirect("bill_list")
    else:
        form = BillForm(instance=bill)
    return render(request, "bill_form.html", {"form": form})

def delete_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    bill.delete()
    return redirect("bill_list")
