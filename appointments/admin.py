from django.contrib import admin

from .models import (
    Department,
    Doctor,
    Patient,
    Appointment,
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "department_id",
        "department_name",
    )
    search_fields = (
        "department_name",
    )


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "doctor_id",
        "doctor_name",
        "specialization",
        "department",
        "is_available",
    )
    list_filter = (
        "department",
        "is_available",
    )
    search_fields = (
        "doctor_name",
        "specialization",
        "email",
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "patient_id",
        "patient_name",
        "email",
        "phone",
    )
    search_fields = (
        "patient_name",
        "email",
        "phone",
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "appointment_id",
        "patient",
        "doctor",
        "appointment_date",
        "status",
    )
    list_filter = (
        "status",
        "appointment_date",
    )
    search_fields = (
        "patient__patient_name",
        "doctor__doctor_name",
    )
