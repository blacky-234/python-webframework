from django.urls import path,include

urlpatterns = [
    path('doctors/', include('urlpatterapp.doctor.urls')),
    path('patients/', include('urlpatterapp.patient.urls')),
]