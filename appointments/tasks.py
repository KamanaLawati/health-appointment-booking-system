import threading

from django.db import close_old_connections
from django.utils import timezone

from .models import Appointment


def complete_overdue_appointments():
    """
    Background task:
    Marks past BOOKED or CONFIRMED appointments as COMPLETED.
    """

    close_old_connections()

    try:
        current_time = timezone.now()

        updated_count = Appointment.objects.filter(
            appointment_date__lt=current_time,
            status__in=[
                "BOOKED",
                "CONFIRMED",
            ]
        ).update(
            status="COMPLETED"
        )

        print(
            f"Background task completed. "
            f"Updated appointments: {updated_count}"
        )

    finally:
        close_old_connections()


def start_appointment_background_task():
    """
    Starts the update task in a separate thread.
    """

    task_thread = threading.Thread(
        target=complete_overdue_appointments,
        daemon=True
    )

    task_thread.start()