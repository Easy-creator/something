from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html', {})

def validate(request):
    return render(request, 'validate.html', {})

def wallet(request):
    return render(request, 'wallet.html', {})