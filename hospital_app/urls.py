from django.urls import path
from . import views

urlpatterns = [
    # Dashboard & Auth
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Doctor CRUD
    path("doctors/", views.doctor_list, name="doctor_list"),
    path("doctors/add/", views.add_doctor, name="add_doctor"),
    path("doctors/edit/<int:pk>/", views.edit_doctor, name="edit_doctor"),
    path('doctors/delete/<int:pk>/', views.delete_doctor, name='delete_doctor'),


    # Patient CRUD
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/edit/<int:pk>/', views.edit_patient, name='edit_patient'),
    path('patients/delete/<int:pk>/', views.delete_patient, name='delete_patient'),


    # Appointment CRUD
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/add/', views.add_appointment, name='add_appointment'),
    path('appointments/edit/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('appointments/delete/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),

    # Treatment CRUD
    path('treatments/', views.treatment_list, name='treatment_list'),
    path('treatments/add/', views.add_treatment, name='add_treatment'),
    path('treatments/edit/<int:treatment_id>/', views.edit_treatment, name='edit_treatment'),
    path('treatments/delete/<int:treatment_id>/', views.delete_treatment, name='delete_treatment'),

    # Bill CRUD
    path('bills/', views.bill_list, name='bill_list'),
    path('bills/add/', views.add_bill, name='add_bill'),
    path('bills/edit/<int:bill_id>/', views.edit_bill, name='edit_bill'),
    path('bills/delete/<int:bill_id>/', views.delete_bill, name='delete_bill'),
]
