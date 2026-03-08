from django.urls import path
from django.http import HttpResponse



urlpatterns = [
    path('doctors/', lambda request: HttpResponse("List of doctors")),
]
