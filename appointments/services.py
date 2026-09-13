from django.db import transaction
from django.utils import timezone

from .models import (
    Department,
    Doctor,
    Patient,
    Appointment,
)


class DepartmentService:

    @staticmethod
    def get_all():
        return Department.objects.all().order_by(
            "department_name"
        )

    @staticmethod
    def get_by_id(department_id):
        return Department.objects.get(
            department_id=department_id
        )

    @staticmethod
    def create(data):
        return Department.objects.create(
            department_name=data["department_name"],
            description=data.get("description")
        )

    @staticmethod
    def update(department_id, data):
        department = DepartmentService.get_by_id(
            department_id
        )

        department.department_name = data.get(
            "department_name",
            department.department_name
        )

        department.description = data.get(
            "description",
            department.description
        )

        department.save(
            force_update=True
        )

        return department

    @staticmethod
    def delete(department_id):
        department = DepartmentService.get_by_id(
            department_id
        )
        department.delete()


class DoctorService:

    @staticmethod
    def get_all():
        return Doctor.objects.select_related(
            "department"
        ).order_by(
            "doctor_name"
        )

    @staticmethod
    def get_by_id(doctor_id):
        return Doctor.objects.select_related(
            "department"
        ).get(
            doctor_id=doctor_id
        )

    @staticmethod
    def get_available_doctors():
        return Doctor.objects.filter(
            is_available=True
        ).select_related(
            "department"
        )

    @staticmethod
    def create(data):
        return Doctor.objects.create(
            department_id=data["department_id"],
            doctor_name=data["doctor_name"],
            specialization=data["specialization"],
            email=data["email"],
            phone=data.get("phone"),
            is_available=data.get(
                "is_available",
                True
            )
        )

    @staticmethod
    def update(doctor_id, data):
        doctor = DoctorService.get_by_id(
            doctor_id
        )

        for field in [
            "doctor_name",
            "specialization",
            "email",
            "phone",
            "is_available",
        ]:
            if field in data:
                setattr(
                    doctor,
                    field,
                    data[field]
                )

        if "department_id" in data:
            doctor.department_id = data[
                "department_id"
            ]

        doctor.save(
            force_update=True
        )

        return doctor

    @staticmethod
    def delete(doctor_id):
        doctor = DoctorService.get_by_id(
            doctor_id
        )
        doctor.delete()


class PatientService:

    @staticmethod
    def get_all():
        return Patient.objects.all().order_by(
            "patient_name"
        )

    @staticmethod
    def get_by_id(patient_id):
        return Patient.objects.get(
            patient_id=patient_id
        )

    @staticmethod
    def create(data):
        return Patient.objects.create(
            patient_name=data["patient_name"],
            date_of_birth=data.get(
                "date_of_birth"
            ),
            gender=data.get("gender"),
            email=data["email"],
            phone=data.get("phone"),
            address=data.get("address")
        )

    @staticmethod
    def update(patient_id, data):
        patient = PatientService.get_by_id(
            patient_id
        )

        for field in [
            "patient_name",
            "date_of_birth",
            "gender",
            "email",
            "phone",
            "address",
        ]:
            if field in data:
                setattr(
                    patient,
                    field,
                    data[field]
                )

        patient.save(
            force_update=True
        )

        return patient

    @staticmethod
    def delete(patient_id):
        patient = PatientService.get_by_id(
            patient_id
        )
        patient.delete()


class AppointmentService:

    @staticmethod
    def get_all():
        return Appointment.objects.select_related(
            "doctor",
            "patient",
        ).order_by(
            "-appointment_date"
        )

    @staticmethod
    def get_by_id(appointment_id):
        return Appointment.objects.select_related(
            "doctor",
            "patient",
        ).get(
            appointment_id=appointment_id
        )

    @staticmethod
    def get_by_status(status):
        return Appointment.objects.filter(
            status=status
        ).select_related(
            "doctor",
            "patient",
        )

    @staticmethod
    @transaction.atomic
    def create(data):
        doctor_id = data["doctor_id"]
        patient_id = data["patient_id"]
        appointment_date = data[
            "appointment_date"
        ]

        doctor = Doctor.objects.get(
            doctor_id=doctor_id
        )

        if not doctor.is_available:
            raise ValueError(
                "This doctor is currently unavailable."
            )

        existing_appointment = Appointment.objects.filter(
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            status__in=[
                "BOOKED",
                "CONFIRMED",
            ]
        ).exists()

        if existing_appointment:
            raise ValueError(
                "This doctor already has an appointment "
                "at that time."
            )

        return Appointment.objects.create(
            doctor_id=doctor_id,
            patient_id=patient_id,
            appointment_date=appointment_date,
            reason=data["reason"],
            status=data.get(
                "status",
                "BOOKED"
            ),
            created_at=timezone.now()
        )

    @staticmethod
    @transaction.atomic
    def update_status(appointment_id, status):
        appointment = AppointmentService.get_by_id(
            appointment_id
        )

        allowed_statuses = [
            "BOOKED",
            "CONFIRMED",
            "COMPLETED",
            "CANCELLED",
        ]

        if status not in allowed_statuses:
            raise ValueError(
                "Invalid appointment status."
            )

        appointment.status = status

        appointment.save(
            force_update=True,
            update_fields=["status"]
        )

        return appointment

    @staticmethod
    def delete(appointment_id):
        appointment = AppointmentService.get_by_id(
            appointment_id
        )
        appointment.delete()

from django.db.models import Count, Q


class AppointmentQueryService:

    # Related Query 1:
    # Find all doctors belonging to a department
    @staticmethod
    def doctors_by_department(department_id):
        return Doctor.objects.filter(
            department_id=department_id
        ).select_related(
            "department"
        ).order_by(
            "doctor_name"
        )

    # Related Query 2:
    # Find all appointments for a specific patient
    @staticmethod
    def appointments_by_patient(patient_id):
        return Appointment.objects.filter(
            patient_id=patient_id
        ).select_related(
            "patient",
            "doctor",
        ).order_by(
            "-appointment_date"
        )

    # Related Query 3:
    # Find all appointments for a specific doctor
    @staticmethod
    def appointments_by_doctor(doctor_id):
        return Appointment.objects.filter(
            doctor_id=doctor_id
        ).select_related(
            "doctor",
            "patient",
        ).order_by(
            "-appointment_date"
        )

    # Complex Query 1:
    # Show appointment details involving:
    # Appointment + Patient + Doctor + Department
    @staticmethod
    def appointment_details():
        return Appointment.objects.select_related(
            "patient",
            "doctor",
            "doctor__department",
        ).order_by(
            "-appointment_date"
        )

    # Complex Query 2:
    # Count appointments for every doctor,
    # including doctors with zero appointments
    @staticmethod
    def doctor_appointment_summary():
        return Doctor.objects.select_related(
            "department"
        ).annotate(
            total_appointments=Count(
                "appointments",
                filter=Q(
                    appointments__status__in=[
                        "BOOKED",
                        "CONFIRMED",
                        "COMPLETED",
                    ]
                )
            )
        ).order_by(
            "-total_appointments",
            "doctor_name"
        )