from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import views as authview
from users.models import users
from workspace.models import workspace
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import json

# Create your views here.

def login_user(request):

    if request.method == 'POST':
        request.session.flush()
        user = authenticate(request,username=request.POST.get('email'), password=request.POST.get('password'))
        login(request, user)
        print("kk: " + str(user))
        print(request.user)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_login = users.objects.get(email=email, password=password)
        if user_login != None:
            request.session['userid'] = user_login.id
            request.session['email'] = user_login.email

            return send_data(request)
        else:
            return render(request, 'login.html', {'error':'Invalid email/password'})
    else:
        
        return render(request, 'login.html', {})

def create_user(email, password, workid):
    try:
        new_user = users.objects.get(email=email)
    except:
        work = {'data':[]}
        new_user = users(email=email, password=password, workspaces=json.dumps(work))
        new_user.save()

    worksp = workspace.objects.get(id=workid)
    channel_json = json.loads(worksp.channels)

    work_json = json.loads(new_user.workspaces)
    work_json['data'].append({'id':workid, 'name': worksp.workspace_name, 'channel_data': json.dumps(work_json)})
    new_user.workspaces = json.dumps(work_json)

    new_user.save()


def register_user(request):
    if request.method == 'POST':
        work = {'data':[]}
        new_user = users(email=request.POST.get('email'), password=request.POST.get('password'), workspaces=json.dumps(work))
        new_user.save()
        user = User.objects.create_user(request.POST.get('email'), request.POST.get('email'), request.POST.get('password'))
        user.save()
        return HttpResponse(new_user.id)
    else:
        return render(request, 'register.html', {})

def log_out(request):
    try:
        del request.session['userid']
        del request.session['email']
    except KeyError:
        pass
    return render(request, 'home.html', {'user': 'Not logged In'})

def append_workspace(userid, id, name, channels):

    #userid = request.session['userid']
    user  = users.objects.get(id=userid)
    print(userid)
    workspace = user.workspaces
    print(type(workspace))
    workspace_json = json.loads(workspace)
    print(type(workspace_json))
    workspace_info = {'id':id, 'name':name, 'channels':json.dumps({'channel_data':[]})}
    workspace_json['data'].append(workspace_info)

    user.workspaces = json.dumps(workspace_json)
    print(user.workspaces)
    user.save()

def insert_channel(work_id, user_id, channel_id, channel_name):
    user = users.objects.get(id=user_id)
    workspace = user.workspaces
    workspace_json = json.loads(workspace)
    for k in workspace_json['data']:
        print(type(k['id']))
        print(type(work_id))
        if k['id'] == int(work_id):
            print('inside work')
            channel_info = k['channels']
            channel_json = json.loads(channel_info)
            channel_data = {'id':channel_id, 'name': channel_name}
            channel_json['channel_data'].append(channel_data)
            k['channels'] = json.dumps(channel_json)
            user.workspaces = json.dumps(workspace_json)
            user.save()



def send_data(request):
    userid = request.session['userid']
    user = users.objects.get(id=userid)
    workspaces = user.workspaces
    workspaces_json = json.loads(workspaces)
    print(type(workspaces))
    print(type(workspaces_json))
    l = []
    id = []
    for data in workspaces_json['data']:
        l.append([data['name'],data['id']])

    cont = {
    'user' : request.session['email'],
    'workspaces': l
    }

    return render(request, 'home.html', context=cont)
