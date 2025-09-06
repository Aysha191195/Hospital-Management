"""from django.shortcuts import render
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

"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.utils.timezone import now, timedelta

from .models import Doctor, Patient, Appointment, Treatment, Bill
from .forms import DoctorForm, PatientForm, AppointmentForm, TreatmentForm, BillForm

# ---------------- Auth ----------------
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created — please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'hospital_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'hospital_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


# ---------------- Dashboard (home) ----------------
@login_required
def home(request):
    # Counts
    patients_count = Patient.objects.count()
    doctors_count = Doctor.objects.count()
    appointments_count = Appointment.objects.count()
    total_revenue = Bill.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    pending_bills = Bill.objects.filter(payment_status='Pending').count()

    # Appointments per doctor (bar chart)
    appt_per_doc_qs = (
        Appointment.objects.values('doctor__name')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    doc_labels = [item['doctor__name'] for item in appt_per_doc_qs]
    doc_counts = [item['count'] for item in appt_per_doc_qs]

    # Appointments last 7 days (line chart)
    today = now().date()
    start_date = today - timedelta(days=6)
    daily_qs = (
        Appointment.objects
        .filter(appointment_date__date__range=[start_date, today])
        .annotate(day=TruncDate('appointment_date'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    # Ensure all 7 days are present
    dates = []
    daily_counts = []
    daily_map = {x['day'].strftime('%Y-%m-%d'): x['count'] for x in daily_qs}
    for i in range(7):
        d = start_date + timedelta(days=i)
        dates.append(d.strftime('%Y-%m-%d'))
        daily_counts.append(daily_map.get(d.strftime('%Y-%m-%d'), 0))

    context = {
        'patients_count': patients_count,
        'doctors_count': doctors_count,
        'appointments_count': appointments_count,
        'total_revenue': total_revenue,
        'pending_bills': pending_bills,
        'doc_labels': doc_labels,
        'doc_counts': doc_counts,
        'dates': dates,
        'daily_counts': daily_counts,
    }
    return render(request, 'hospital_app/home.html', context)


# ---------------- Doctors (CRUD + search + pagination) ----------------
@login_required
def doctor_list(request):
    q = request.GET.get('q','')
    qs = Doctor.objects.filter(name__icontains=q) if q else Doctor.objects.all()
    paginator = Paginator(qs.order_by('name'), 10)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'hospital_app/doctor_list.html', {'doctors': page, 'query': q})

@login_required
def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    return render(request, 'hospital_app/add_doctor.html', {'form': form})

@login_required
def edit_doctor(request, doctor_id):
    obj = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm(instance=obj)
    return render(request, 'hospital_app/edit_doctor.html', {'form': form})

@login_required
def delete_doctor(request, doctor_id):
    obj = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        obj.delete()
        return redirect('doctor_list')
    return render(request, 'hospital_app/delete_confirm.html', {'object': obj, 'type': 'Doctor'})


# ---------------- Patients ----------------
@login_required
def patient_list(request):
    q = request.GET.get('q','')
    qs = Patient.objects.filter(name__icontains=q) if q else Patient.objects.all()
    paginator = Paginator(qs.order_by('name'), 10)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'hospital_app/patient_list.html', {'patients': page, 'query': q})

@login_required
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'hospital_app/add_patient.html', {'form': form})

@login_required
def edit_patient(request, patient_id):
    obj = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=obj)
    return render(request, 'hospital_app/edit_patient.html', {'form': form})

@login_required
def delete_patient(request, patient_id):
    obj = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        obj.delete()
        return redirect('patient_list')
    return render(request, 'hospital_app/delete_confirm.html', {'object': obj, 'type': 'Patient'})


# ---------------- Appointments ----------------
@login_required
def appointment_list(request):
    q = request.GET.get('q','')
    qs = Appointment.objects.filter(patient__name__icontains=q) if q else Appointment.objects.all()
    paginator = Paginator(qs.order_by('-appointment_date'), 10)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'hospital_app/appointment_list.html', {'appointments': page, 'query': q})

@login_required
def add_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'hospital_app/add_appointment.html', {'form': form})

@login_required
def edit_appointment(request, appointment_id):
    obj = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=obj)
    return render(request, 'hospital_app/edit_appointment.html', {'form': form})

@login_required
def delete_appointment(request, appointment_id):
    obj = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        obj.delete()
        return redirect('appointment_list')
    return render(request, 'hospital_app/delete_confirm.html', {'object': obj, 'type': 'Appointment'})


# ---------------- Treatments & Bills (basic create forms) ----------------
@login_required
def add_treatment(request):
    if request.method == 'POST':
        form = TreatmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Treatment saved.")
            return redirect('appointment_list')
    else:
        form = TreatmentForm()
    return render(request, 'hospital_app/add_treatment.html', {'form': form})

@login_required
def add_bill(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Bill saved.")
            return redirect('appointment_list')
    else:
        form = BillForm()
    return render(request, 'hospital_app/add_bill.html', {'form': form})
