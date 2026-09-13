from django.db import models


class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(
        max_length=100,
        unique=True
    )
    description = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = "DEPARTMENTS"

    def __str__(self):
        return self.department_name


class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        db_column="DEPARTMENT_ID",
        related_name="doctors"
    )

    doctor_name = models.CharField(max_length=150)
    specialization = models.CharField(max_length=150)

    email = models.EmailField(
        unique=True,
        max_length=150
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    is_available = models.BooleanField(
        default=True
    )

    class Meta:
        managed = False
        db_table = "DOCTORS"

    def __str__(self):
        return f"Dr. {self.doctor_name}"


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=150)

    date_of_birth = models.DateField(
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    email = models.EmailField(
        unique=True,
        max_length=150
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    address = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = "PATIENTS"

    def __str__(self):
        return self.patient_name


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("BOOKED", "Booked"),
        ("CONFIRMED", "Confirmed"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    appointment_id = models.AutoField(primary_key=True)

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.PROTECT,
        db_column="DOCTOR_ID",
        related_name="appointments"
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        db_column="PATIENT_ID",
        related_name="appointments"
    )

    appointment_date = models.DateTimeField()
    reason = models.CharField(max_length=500)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="BOOKED"
    )

    created_at = models.DateTimeField(
        auto_now_add=False
    )

    class Meta:
        managed = False
        db_table = "APPOINTMENTS"

    def __str__(self):
        return (
            f"{self.patient.patient_name} - "
            f"{self.doctor.doctor_name} - "
            f"{self.appointment_date}"
        )