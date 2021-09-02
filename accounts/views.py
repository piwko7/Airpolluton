from django.shortcuts import render, redirect

# Create your views here.


def register(request):
    context = {}
    return render(request, 'accounts/register.html', context)

def login_view(request):
    context = {}
    return render(request, 'accounts/login.html', context)

def logout_view(request):
    return redirect('accounts:login')

