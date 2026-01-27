from django.shortcuts import render

# Create your views here.


class Auth:


    def Root_Views(request):

        return render(request, 'rootpage/index.html')