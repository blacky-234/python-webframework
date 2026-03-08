from django.urls import path
from django.http import HttpResponse


urlpatterns = [
    path('patients/', lambda request: HttpResponse("List of patients")),
]