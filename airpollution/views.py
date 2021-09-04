from django.shortcuts import render

# Create your views here.

# from .models import


def welcome(request):
    context = {
        'page': request.path
    }
    return render(request, 'airpollution/welcome.html', context)
