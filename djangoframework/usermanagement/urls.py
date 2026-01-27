from django.urls import path
from .views import Auth

Auth = [
    path('', Auth.Root_Views, name='login'),
]



urlpatterns = Auth