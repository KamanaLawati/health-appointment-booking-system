from rest_framework import serializers

from .models import (
    Department,
    Doctor,
    Patient,
    Appointment,
)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "department_id",
            "department_name",
            "description",
        ]


class DoctorSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(
        source="department.department_name",
        read_only=True
    )

    class Meta:
        model = Doctor
        fields = [
            "doctor_id",
            "department",
            "department_name",
            "doctor_name",
            "specialization",
            "email",
            "phone",
            "is_available",
        ]


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "patient_id",
            "patient_name",
            "date_of_birth",
            "gender",
            "email",
            "phone",
            "address",
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(
        source="patient.patient_name",
        read_only=True
    )

    doctor_name = serializers.CharField(
        source="doctor.doctor_name",
        read_only=True
    )

    class Meta:
        model = Appointment
        fields = [
            "appointment_id",
            "patient",
            "patient_name",
            "doctor",
            "doctor_name",
            "appointment_date",
            "reason",
            "status",
            "created_at",
        ]
        read_only_fields = [
            "appointment_id",
            "created_at",
        ]