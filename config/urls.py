from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),

    # All web pages and API routes
    path(
        "",
        include("appointments.urls")
    ),
]
