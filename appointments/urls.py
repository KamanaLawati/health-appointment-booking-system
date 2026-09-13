from django.urls import path

from .views import (
    home_page,
    doctors_page,
    patients_page,
    patient_create_page,
    appointments_page,
    appointment_create_page,
    appointment_status_page,
    appointment_report_page,

    DepartmentListCreateView,
    DepartmentDetailView,
    DoctorListCreateView,
    DoctorDetailView,
    PatientListCreateView,
    PatientDetailView,
    AppointmentListCreateView,
    AppointmentDetailView,
    AppointmentStatusUpdateView,
    AppointmentReportsView,
    RunAppointmentBackgroundTaskView,
)


urlpatterns = [
    # Web pages
    path("", home_page, name="home-page"),
    path("doctors/", doctors_page, name="doctors-page"),
    path("patients/", patients_page, name="patients-page"),
    path(
        "patients/create/",
        patient_create_page,
        name="patient-create-page"
    ),
    path(
        "appointments/",
        appointments_page,
        name="appointments-page"
    ),
    path(
        "appointments/create/",
        appointment_create_page,
        name="appointment-create-page"
    ),

    # API endpoints
    path(
        "api/departments/",
        DepartmentListCreateView.as_view(),
        name="department-list-create"
    ),
    path(
        "api/departments/<int:department_id>/",
        DepartmentDetailView.as_view(),
        name="department-detail"
    ),
    path(
        "api/doctors/",
        DoctorListCreateView.as_view(),
        name="doctor-list-create"
    ),
    path(
        "api/doctors/<int:doctor_id>/",
        DoctorDetailView.as_view(),
        name="doctor-detail"
    ),
    path(
        "api/patients/",
        PatientListCreateView.as_view(),
        name="patient-list-create"
    ),
    path(
        "api/patients/<int:patient_id>/",
        PatientDetailView.as_view(),
        name="patient-detail"
    ),
    path(
        "api/appointments/",
        AppointmentListCreateView.as_view(),
        name="appointment-list-create"
    ),
    path(
        "api/appointments/<int:appointment_id>/",
        AppointmentDetailView.as_view(),
        name="appointment-detail"
    ),
    path(
        "api/appointments/<int:appointment_id>/status/",
        AppointmentStatusUpdateView.as_view(),
        name="appointment-status-update"
    ),
    path(
        "api/reports/appointments/",
        AppointmentReportsView.as_view(),
        name="appointment-reports"
    ),
    path(
        "api/tasks/complete-overdue/",
        RunAppointmentBackgroundTaskView.as_view(),
        name="run-background-task"
    ),
    path(
        "appointments/<int:appointment_id>/status/",
        appointment_status_page,
        name="appointment-status-page"
    ),
    path(
        "reports/",
        appointment_report_page,
        name="appointment-report-page"
    ),
]