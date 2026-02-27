from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.



class testing:

    @api_view(['GET'])
    def learning_view(request):
        data = {
            'message': 'Welcome to the learning app!'
        }
        return Response(data)