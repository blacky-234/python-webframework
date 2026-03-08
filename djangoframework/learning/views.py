from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet,ModelViewSet,GenericViewSet,ReadOnlyModelViewSet,ViewSetMixin

# Create your views here.



class testing(ViewSet):

    def list(self, request):
        return Response({"message":"hello world"})
    
    def retrive(self, request, pk=None):
        return Response({"message":"hello world"})