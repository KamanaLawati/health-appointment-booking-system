from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .services import AppointmentQueryService
from .services import AppointmentService
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .tasks import start_appointment_background_task

from .models import (
    Department,
    Doctor,
    Patient,
    Appointment,
)

from .serializers import (
    DepartmentSerializer,
    DoctorSerializer,
    PatientSerializer,
    AppointmentSerializer,
)

from .services import (
    DepartmentService,
    DoctorService,
    PatientService,
    AppointmentService,
    AppointmentQueryService,
)


class DepartmentListCreateView(APIView):

    def get(self, request):
        departments = DepartmentService.get_all()

        serializer = DepartmentSerializer(
            departments,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = DepartmentSerializer(
            data=request.data
        )

        if serializer.is_valid():
            department = DepartmentService.create(
                serializer.validated_data
            )

            return Response(
                DepartmentSerializer(department).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class AppointmentReportsView(APIView):

    def get(self, request):
        details = (
            AppointmentQueryService
            .appointment_details()
        )

        data = []

        for appointment in details:
            data.append({
                "appointment_id": appointment.appointment_id,
                "appointment_date": appointment.appointment_date,
                "patient_name": (
                    appointment.patient.patient_name
                ),
                "doctor_name": (
                    appointment.doctor.doctor_name
                ),
                "specialization": (
                    appointment.doctor.specialization
                ),
                "department_name": (
                    appointment.doctor.department.department_name
                ),
                "status": appointment.status,
            })

        return Response(data)

        
class DepartmentDetailView(APIView):

    def get(self, request, department_id):
        department = get_object_or_404(
            Department,
            department_id=department_id
        )

        return Response(
            DepartmentSerializer(department).data
        )

    def put(self, request, department_id):
        serializer = DepartmentSerializer(
            data=request.data
        )

        if serializer.is_valid():
            department = DepartmentService.update(
                department_id,
                serializer.validated_data
            )

            return Response(
                DepartmentSerializer(department).data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, department_id):
        DepartmentService.delete(department_id)

        return Response(
            {
                "message": "Department deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )


class DoctorListCreateView(APIView):

    def get(self, request):
        doctors = DoctorService.get_all()

        serializer = DoctorSerializer(
            doctors,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = DoctorSerializer(
            data=request.data
        )

        if serializer.is_valid():
            doctor = DoctorService.create(
                serializer.validated_data
            )

            return Response(
                DoctorSerializer(doctor).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class DoctorDetailView(APIView):

    def get(self, request, doctor_id):
        doctor = DoctorService.get_by_id(doctor_id)

        return Response(
            DoctorSerializer(doctor).data
        )

    def put(self, request, doctor_id):
        doctor = DoctorService.get_by_id(doctor_id)

        serializer = DoctorSerializer(
            doctor,
            data=request.data
        )

        if serializer.is_valid():
            updated_doctor = DoctorService.update(
                doctor_id,
                serializer.validated_data
            )

            return Response(
                DoctorSerializer(updated_doctor).data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, doctor_id):
        DoctorService.delete(doctor_id)

        return Response(
            {
                "message": "Doctor deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )


class PatientListCreateView(APIView):

    def get(self, request):
        patients = PatientService.get_all()

        serializer = PatientSerializer(
            patients,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = PatientSerializer(
            data=request.data
        )

        if serializer.is_valid():
            patient = PatientService.create(
                serializer.validated_data
            )

            return Response(
                PatientSerializer(patient).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class PatientDetailView(APIView):

    def get(self, request, patient_id):
        patient = PatientService.get_by_id(patient_id)

        return Response(
            PatientSerializer(patient).data
        )

    def put(self, request, patient_id):
        patient = PatientService.get_by_id(patient_id)

        serializer = PatientSerializer(
            patient,
            data=request.data
        )

        if serializer.is_valid():
            updated_patient = PatientService.update(
                patient_id,
                serializer.validated_data
            )

            return Response(
                PatientSerializer(updated_patient).data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, patient_id):
        PatientService.delete(patient_id)

        return Response(
            {
                "message": "Patient deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )


class AppointmentListCreateView(APIView):

    def get(self, request):
        appointments = AppointmentService.get_all()

        serializer = AppointmentSerializer(
            appointments,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = AppointmentSerializer(
            data=request.data
        )

        if serializer.is_valid():
            try:
                appointment = AppointmentService.create(
                    serializer.validated_data
                )

                return Response(
                    AppointmentSerializer(appointment).data,
                    status=status.HTTP_201_CREATED
                )

            except ValueError as error:
                return Response(
                    {
                        "error": str(error)
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class AppointmentDetailView(APIView):

    def get(self, request, appointment_id):
        appointment = AppointmentService.get_by_id(
            appointment_id
        )

        return Response(
            AppointmentSerializer(appointment).data
        )

    def delete(self, request, appointment_id):
        AppointmentService.delete(appointment_id)

        return Response(
            {
                "message": "Appointment deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )


class AppointmentStatusUpdateView(APIView):

    def patch(self, request, appointment_id):
        new_status = request.data.get("status")

        if not new_status:
            return Response(
                {
                    "error": "status is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            appointment = (
                AppointmentService.update_status(
                    appointment_id,
                    new_status
                )
            )

            return Response(
                AppointmentSerializer(appointment).data
            )

        except ValueError as error:
            return Response(
                {
                    "error": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

from .models import Doctor, Patient, Appointment
from .services import PatientService, AppointmentService


def home_page(request):
    return render(
        request,
        "appointments/home.html"
    )


def doctors_page(request):
    doctors = DoctorService.get_available_doctors()

    return render(
        request,
        "appointments/doctors.html",
        {
            "doctors": doctors
        }
    )


def patients_page(request):
    patients = PatientService.get_all()

    return render(
        request,
        "appointments/patients.html",
        {
            "patients": patients
        }
    )


def patient_create_page(request):
    if request.method == "POST":
        data = {
            "patient_name": request.POST.get(
                "patient_name"
            ),
            "date_of_birth": request.POST.get(
                "date_of_birth"
            ) or None,
            "gender": request.POST.get(
                "gender"
            ),
            "email": request.POST.get(
                "email"
            ),
            "phone": request.POST.get(
                "phone"
            ),
            "address": request.POST.get(
                "address"
            ),
        }

        try:
            PatientService.create(data)

            messages.success(
                request,
                "Patient registered successfully."
            )

            return redirect("patients-page")

        except Exception as error:
            messages.error(
                request,
                f"Unable to register patient: {error}"
            )

    return render(
        request,
        "appointments/patient_form.html"
    )


def appointments_page(request):
    appointments = AppointmentService.get_all()

    return render(
        request,
        "appointments/appointments.html",
        {
            "appointments": appointments
        }
    )


def appointment_create_page(request):
    doctors = DoctorService.get_available_doctors()
    patients = PatientService.get_all()

    if request.method == "POST":
        data = {
            "doctor_id": request.POST.get(
                "doctor_id"
            ),
            "patient_id": request.POST.get(
                "patient_id"
            ),
            "appointment_date": request.POST.get(
                "appointment_date"
            ),
            "reason": request.POST.get(
                "reason"
            ),
            "status": "BOOKED",
        }

        try:
            AppointmentService.create(data)

            messages.success(
                request,
                "Appointment booked successfully."
            )

            return redirect("appointments-page")

        except Exception as error:
            messages.error(
                request,
                f"Unable to book appointment: {error}"
            )

    return render(
        request,
        "appointments/appointment_form.html",
        {
            "doctors": doctors,
            "patients": patients,
        }
    )

class RunAppointmentBackgroundTaskView(APIView):

    def post(self, request):
        start_appointment_background_task()

        return Response(
            {
                "message": (
                    "Appointment background task "
                    "started successfully."
                )
            },
            status=status.HTTP_202_ACCEPTED
        )

def appointment_status_page(request, appointment_id):
    appointment = AppointmentService.get_by_id(
        appointment_id
    )

    if request.method == "POST":
        new_status = request.POST.get("status")

        try:
            AppointmentService.update_status(
                appointment_id,
                new_status
            )

            messages.success(
                request,
                "Appointment status updated successfully."
            )

            return redirect("appointments-page")

        except ValueError as error:
            messages.error(
                request,
                str(error)
            )

    return render(
        request,
        "appointments/appointment_status_form.html",
        {
            "appointment": appointment
        }
    )

def appointment_report_page(request):
    report_data = (
        AppointmentQueryService
        .appointment_details()
    )

    return render(
        request,
        "appointments/appointment_report.html",
        {
            "report_data": report_data
        }
    )