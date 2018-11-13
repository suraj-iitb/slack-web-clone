from django.shortcuts import render, redirect
from .models import Workspace, Channel
from Messages.models import Message, Replies
from Users.models import User
from django.contrib.auth.models import User as Admin_User
from django.conf import settings
from django.core.mail import send_mail

import uuid
# Create your views here.

def show_workspaces(request):

    if request.user.is_authenticated:
        print(request.user.is_authenticated)
        userid = request.session['userid']
        user = User.objects.get(id=userid)
        print(user)
        workspaces = user.workspace_set.all()
        print(workspaces)
        workp = []
        for work in workspaces:
            workp.append([work.id,work.name])
        cont = {
            'workspaces': workp,
        }
        return render(request, 'entry.html', context=cont)
    else:
        return redirect('http://127.0.0.1:8000/login/')

def create_workspace(request):
    name = request.POST.get('name')
    worksp = Workspace.objects.create(name=name)
    user = User.objects.get(id=request.session['userid'])
    print(user.email)
    worksp.users.add(user)
    worksp.admin.add(user)

    return redirect('http://127.0.0.1:8000/workspace/')

def get_random_password():
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:6]

def accept_invite(request,  workspace_id, email, password):
    user = User.objects.create(name=email, email=email,password=password,isfirst=True)

    ad_user = Admin_User.objects.create_user(email, email, password)
    ad_user.save()
    workspace = Workspace.objects.get(id=workspace_id)
    workspace.users.add(user)
    return redirect('http://127.0.0.1:8000/login/')

def invite_user(request, workspace_id):
    try:
        user = User.objects.get(email=request.POST.get('email'))
        workspace = Workspace.objects.get(id=workspace_id)
        workspace.users.add(user)
    except:
        subject = 'Slack : Invited to a Workspace'
        passw = get_random_password()
        message = 'You have been invited to the following workspace. Click the link below to accept\n'
        message = message + 'http://127.0.0.1:8000/workspace/accept/' + workspace_id + "/" + request.POST['email'] + "/" + ""+passw+'\n'
        message = message + "\nPassword: " + passw
        email_from = settings.EMAIL_HOST_USER

        recipient_list = [request.POST.get('email')]
        send_mail(subject, message, email_from, recipient_list)
    return redirect('http://127.0.0.1:8000/workspace/'+workspace_id)

def show_messages(request, workspace_id, channel_id):
    print("Heredo")
    print(workspace_id)
    try:
        message = Message.objects.filter(channels=Channel.objects.get(id=channel_id))
        content_a = []
        print("here")
        print(message)
        for mess in message:
            content_a.append([mess.id, mess.user.name,mess.content])
    except Exception as e:
        print(e)
        content_a = ""

    return show_channels(request, workspace_id, content_a, channel_id, get_last_id())

def create_channel(request, workspace_id):
    name = request.POST.get('channel_name')
    print(name)
    work = Workspace.objects.get(id=workspace_id)
    channel = Channel.objects.create(name=name, workspaces=work)
    work = Workspace.objects.get(id=workspace_id)


    return show_channels(request, workspace_id)

def remove_user(request, work_id, user_id):
    work = Workspace.objects.get(id=work_id)
    work.users.remove(User.objects.get(id=user_id))
    return show_channels(request, work_id)


def oneonerender(request, userid):
    user2id = request.session['userid']
    ak = ""
    if int(userid) < int(user2id):
        ak = str(userid)+str(user2id)
    else:
        ak = str(user2id)+str(userid)

    cont = {
        'id': ak,
    }
    return render(request, 'oneone.html', context=cont)
def save_reply(reply, message_id, email):
    mess = Message.objects.get(id=message_id)
    user = User.objects.get(email=email)
    rep = Replies.objects.create(content=reply, message=mess, user=user)

def show_thread(request, message_id):
    mess = Message.objects.get(id=message_id)
    message = mess.content
    repl = Replies.objects.filter(message=mess)
    replies = []
    for rep in repl:
        replies.append([rep.user,rep.id, rep.content])

    return render(request, 'thread.html', {'replies':replies, 'message':message,'message_id':message_id})

def remove_channel(request, workid, channelid):
    Channel.objects.get(id=channelid).delete()
    return show_channels(request, workspace_id=workid)

def show_channels(request, workspace_id, message="", channel_id=0,lastid=0, isadmin=False):
    workspace = Workspace.objects.get(id=workspace_id)
    channels = workspace.channel_set.all()
    chanp = []
    for chan in channels:
        chanp.append([chan.id,chan.name])
    users = []
    u = workspace.users.all()

    for uu in u:
        users.append([uu.id,uu.name])
    userid = request.session['userid']
    try:
        work = workspace.admin.get(id=userid)
        isadmin = True
    except Exception as e:
        isadmin = False
    print(isadmin)
    cont = {
        'users': users,
        'id': workspace_id,
        'last_id': lastid,
        'channel_id': channel_id,
        'channels': chanp,
        'messages': message,
        'isadmin': isadmin,
    }
    print(cont)
    return render(request, 'workspace.html', context=cont)

def get_last_id():
    try:
        last_id = int(Message.objects.latest('id').id) + 1
        return last_id
    except:
        return 0
