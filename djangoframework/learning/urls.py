from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import testing

check = DefaultRouter()

check.register(r'testing', testing, basename='testing')

checking = [
    path('api/', include('learning.urls')),
]

urlpatterns = checking
